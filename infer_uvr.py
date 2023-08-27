import os
import shutil
import sys
import traceback
import torch

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["no_proxy"] = "localhost, 127.0.0.1, ::1"

import ffmpeg
from infer_uvr5 import _audio_pre_, _audio_pre_new

now_dir = os.getcwd()
sys.path.append(now_dir)
tmp = os.path.join(now_dir, "TEMP")
# shutil.rmtree(tmp, ignore_errors=True)
shutil.rmtree("%s/runtime/Lib/site-packages/infer_pack" % (now_dir), ignore_errors=True)
shutil.rmtree("%s/runtime/Lib/site-packages/uvr5_pack" % (now_dir), ignore_errors=True)
os.makedirs(tmp, exist_ok=True)
os.makedirs(os.path.join(now_dir, "logs"), exist_ok=True)
os.makedirs(os.path.join(now_dir, "weights"), exist_ok=True)
os.environ["TEMP"] = tmp
torch.manual_seed(114514)

weight_root = "weights"
weight_uvr5_root = "uvr5_weights"
index_root = "logs"

def uvr(model_name, inp_root, save_root_vocal, paths, save_root_ins, agg, format0):
    infos = []
    try:
        inp_root = inp_root.strip(" ").strip('"').strip("\n").strip('"').strip(" ")
        save_root_vocal = save_root_vocal.strip(" ").strip('"').strip("\n").strip('"').strip(" ")
        save_root_ins = save_root_ins.strip(" ").strip('"').strip("\n").strip('"').strip(" ")

        if model_name == "onnx_dereverb_By_FoxJoy":
            from MDXNet import MDXNetDereverb
            pre_fun = MDXNetDereverb(15)
        else:
            func = _audio_pre_ if "DeEcho" not in model_name else _audio_pre_new
            pre_fun = func(
                agg=int(agg),
                model_path=os.path.join(weight_uvr5_root, model_name + ".pth"),
                device="cuda",
                is_half=True
            )
        
        need_reformat = 1
        done = 0
        try:
            info = ffmpeg.probe(inp_root, cmd="ffprobe")
            if (info["streams"][0]["channels"] == 2 and info["streams"][0]["sample_rate"] == "44100"):
                need_reformat = 0
                pre_fun._path_audio_(inp_root, save_root_ins, save_root_vocal, format0)
                done = 1
        except:
            need_reformat = 1
            infos.append(traceback.format_exc())

        if need_reformat == 1:
            tmp_path = os.path.join(tmp, "{}.reformatted.wav".format(os.path.basename(inp_root)))
            
            # Wrap paths in double quotes to handle spaces
            os.system('ffmpeg -i "{}" -vn -acodec pcm_s16le -ac 2 -ar 44100 "{}" -y'.format(inp_root, tmp_path))
            
            inp_root = tmp_path

        try:
            if done == 0:
                pre_fun._path_audio_(inp_root, save_root_ins, save_root_vocal, format0)
            infos.append("{}->Success".format(os.path.basename(inp_root)))
        except:
            infos.append("{}->{}".format(os.path.basename(inp_root), traceback.format_exc()))
            
    except Exception as e:
        infos.append(traceback.format_exc())

    finally:
        try:
            if model_name == "onnx_dereverb_By_FoxJoy":
                del pre_fun.pred.model
                del pre_fun.pred.model_
            else:
                del pre_fun.model
                del pre_fun
        except:
            infos.append(traceback.format_exc())

        print("clean_empty_cache")
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    for info in infos:
        print(info)

if __name__ == "__main__":
    uvr(model_name="5_HP-Karaoke-UVR",
        inp_root="songs\heythere.mp4",
        save_root_vocal="opt", 
        paths="",
        save_root_ins="opt",
        agg=10,
        format0="wav")