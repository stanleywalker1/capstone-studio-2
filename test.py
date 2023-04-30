from pyodide import to_js, create_proxy
from PIL import Image
import io
import time
import base64
from collections import deque
import numpy as np
from js import (
    console,
    document,
    parent,
    devicePixelRatio,
    ImageData,
    Uint8ClampedArray,
    CanvasRenderingContext2D as Context2d,
    requestAnimationFrame,
    window,
    encodeURIComponent,
    w2ui,
    update_eraser,
    update_scale,
    adjust_selection,
    update_count,
    enable_result_lst,
    setup_shortcut,
    update_undo_redo,
    alert,
    uploadImageToFirebase,
    firebase,
    aws,
)
answer = aws("hello", 1, 2)
console.log(answer)

#addPhoto("demo")

# async def get_latest_image_from_firebase():
    # alert("get_latest_image_from_firebase called")

    # try:
        # database = firebase.database()
        # alert("try called")
        # latestImageRef = database.ref("latestImage")
        # latestImageSnapshot = await latestImageRef.once("value")
        # latestImageInfo = latestImageSnapshot.val()

      
        # download_url = latestImageInfo["downloadURL"]

       
        # with pyodide.open_url(download_url) as f:
           
            # img = Image.open(f)

        # print("Downloaded image:", str(img))
        # return img
    # except Exception as e:
        # print("Error while getting the latest image from Firebase:", str(e))
        # return None


from canvas import InfCanvas


class History:
    def __init__(self,maxlen=10):
        self.idx=-1
        self.undo_lst=deque([],maxlen=maxlen)
        self.redo_lst=deque([],maxlen=maxlen)
        self.state=None

    def undo(self):
        cur=None
        if len(self.undo_lst):
            cur=self.undo_lst.pop()
            self.redo_lst.appendleft(cur)
        return cur
    def redo(self):
        cur=None
        if len(self.redo_lst):
            cur=self.redo_lst.popleft()
            self.undo_lst.append(cur)
        return cur

    def check(self):
        return len(self.undo_lst)>0,len(self.redo_lst)>0

    def append(self,state,update=True):
        self.redo_lst.clear()
        self.undo_lst.append(state)
        if update:
            update_undo_redo(*self.check())

history = History()

base_lst = [None]
async def draw_canvas() -> None:
    alert("draw_canvas called")
    width=1024
    height=700
    canvas=InfCanvas(1024,700)
    update_eraser(canvas.eraser_size,min(canvas.selection_size_h,canvas.selection_size_w))
    document.querySelector("#container").style.height= f"{height}px"
    document.querySelector("#container").style.width = f"{width}px"
    canvas.setup_mouse()
    canvas.clear_background()
    canvas.draw_buffer()
    canvas.draw_selection_box()
    base_lst[0]=canvas

    # latest_image = await get_latest_image_from_firebase()

    # if latest_image is not None:
        # Log the URL of the latest image to the console
        # console.log(f"Latest image URL: {latest_image.url}")
        # Request the parent window to display the latest image on the canvas
        # (commented out to fix the indentation error)
        # window.parent.postMessage({ type: "displayLatestImageOnCanvas", image: latest_image }, "*")
    # else:
        # print("No latest image found in Firebase.")


async def draw_canvas_func(event):
    alert("draw_canvas gradio called")
    try:
        app=parent.document.querySelector("gradio-app")
        if app.shadowRoot:
            app=app.shadowRoot
        width=app.querySelector("#canvas_width input").value
        height=app.querySelector("#canvas_height input").value
        selection_size=app.querySelector("#selection_size input").value
    except:
        width=1024
        height=768
        selection_size=384
    document.querySelector("#container").style.width = f"{width}px"
    document.querySelector("#container").style.height= f"{height}px"
    canvas=InfCanvas(int(width),int(height),selection_size=int(selection_size))
    canvas.setup_mouse()
    canvas.clear_background()
    canvas.draw_buffer()
    canvas.draw_selection_box()
    base_lst[0]=canvas

    # latest_image = await get_latest_image_from_firebase()

    # if latest_image is not None:
        # alert("if called");
        # Log the URL of the latest image to the console
        # console.log(f"Latest image URL: {latest_image.url}")
        # Request the parent window to display the latest image on the canvas
        # (commented out to fix the indentation error)
        # window.parent.postMessage({ type: "displayLatestImageOnCanvas", image: latest_image }, "*")
    # else:
        # print("No latest image found in Firebase.")
        # alert("else called");

import js 

async def export_func(event):
    base = base_lst[0]

    arr = base.export()
    base.draw_buffer()
    base.canvas[2].clear()
    base64_str = base.numpy_to_base64(arr)
    time_str = time.strftime("%Y%m%d_%H%M%S")

    # The rest of the original export_func code
    link = document.createElement("a")
    if len(event.data) > 2 and event.data[2]:
        filename = event.data[2]
    else:
        filename = f"outpaint_{time_str}"
    link.download = f"{filename}.png"
    link.href = "data:image/png;base64," + base64_str
    link.click()
    console.log(f"Canvas saved to {filename}.png")

img_candidate_lst=[None,0]

async def outpaint_func(event):
    base=base_lst[0]
    if len(event.data)==2:
        app=parent.document.querySelector("gradio-app")
        if app.shadowRoot:
            app=app.shadowRoot
        base64_str_raw=app.querySelector("#output textarea").value
        base64_str_lst=base64_str_raw.split(",")
        img_candidate_lst[0]=base64_str_lst
        img_candidate_lst[1]=0
    elif event.data[2]=="next":
        img_candidate_lst[1]+=1
    elif event.data[2]=="prev":
        img_candidate_lst[1]-=1
    enable_result_lst()
    if img_candidate_lst[0] is None:
        return
    lst=img_candidate_lst[0]
    idx=img_candidate_lst[1]
    update_count(idx%len(lst)+1,len(lst))
    arr=base.base64_to_numpy(lst[idx%len(lst)])
    base.fill_selection(arr)
    base.draw_selection_box()

async def undo_func(event):
    base=base_lst[0]
    img_candidate_lst[0]=None
    if base.sel_dirty:
        base.sel_buffer = np.zeros((base.selection_size_h, base.selection_size_w, 4), dtype=np.uint8)
        base.sel_dirty = False
    base.canvas[2].clear()

async def commit_func(event):
    base = base_lst[0]
    img_candidate_lst[0] = None
    if base.sel_dirty:
        base.write_selection_to_buffer()
        base.draw_buffer()
    base.canvas[2].clear()
    if len(event.data) > 2:
        history.append(base.save())

    # Add the image uploading code here
    arr = base.export()
    base64_str = base.numpy_to_base64(arr)
    time_str = time.strftime("%Y%m%d_%H%M%S")

    # Call the JavaScript function to upload the image to Firebase storage
    await js.uploadImageToFirebase(base64_str, time_str)
    

async def history_undo_func(event):
    base=base_lst[0]
    if base.buffer_dirty or len(history.redo_lst)>0:
        state=history.undo()
    else:
        history.undo()
        state=history.undo()
    if state is not None:
        base.load(state)
    update_undo_redo(*history.check())
    
async def history_setup_func(event):
    base=base_lst[0]
    history.undo_lst.clear()
    history.redo_lst.clear()
    history.append(base.save(),update=False)

async def history_redo_func(event):
    base=base_lst[0]
    if len(history.undo_lst)>0:
        state=history.redo()
    else:
        history.redo()
        state=history.redo()
    if state is not None:
        base.load(state)
    update_undo_redo(*history.check())


async def transfer_func(event):
    base=base_lst[0]
    base.read_selection_from_buffer()
    sel_buffer=base.sel_buffer
    sel_buffer_str=base.numpy_to_base64(sel_buffer)
    app=parent.document.querySelector("gradio-app")
    if app.shadowRoot:
        app=app.shadowRoot
    app.querySelector("#input textarea").value=sel_buffer_str
    app.querySelector("#proceed").click()

async def upload_func(event):
    base=base_lst[0]
    # base64_str=event.data[1]
    base64_str=document.querySelector("#upload_content").value
    base64_str=base64_str.split(",")[-1]
    # base64_str=parent.document.querySelector("gradio-app").shadowRoot.querySelector("#upload textarea").value
    arr=base.base64_to_numpy(base64_str)
    h,w,c=base.buffer.shape
    base.sync_to_buffer()
    base.buffer_dirty=True
    mask=arr[:,:,3:4].repeat(4,axis=2)
    base.buffer[mask>0]=0
    # in case mismatch
    base.buffer[0:h,0:w,:]+=arr
    #base.buffer[yo:yo+h,xo:xo+w,0:3]=arr[:,:,0:3]
    #base.buffer[yo:yo+h,xo:xo+w,-1]=arr[:,:,-1]
    base.draw_buffer()
    if len(event.data)>2:
        history.append(base.save())

async def setup_shortcut_func(event):
    setup_shortcut(event.data[1])
  

document.querySelector("#export").addEventListener("click",create_proxy(export_func))
document.querySelector("#undo").addEventListener("click",create_proxy(undo_func))
document.querySelector("#commit").addEventListener("click",create_proxy(commit_func))
document.querySelector("#outpaint").addEventListener("click",create_proxy(outpaint_func))
document.querySelector("#upload").addEventListener("click",create_proxy(upload_func))

document.querySelector("#transfer").addEventListener("click",create_proxy(transfer_func))
document.querySelector("#draw").addEventListener("click",create_proxy(draw_canvas_func))

async def setup_func():
    document.querySelector("#setup").value="1"

async def reset_func(event):
    base=base_lst[0]
    base.reset()
    
async def load_func(event):
    base=base_lst[0]
    base.load(event.data[1])

async def save_func(event):
    base=base_lst[0]
    json_str=base.save()
    time_str = time.strftime("%Y%m%d_%H%M%S")
    link = document.createElement("a")
    if len(event.data)>2 and event.data[2]:
        filename = str(event.data[2]).strip()
    else:
        filename = f"outpaint_{time_str}"
    # link.download = f"sdinf_state_{time_str}.json"
    link.download = f"{filename}.sdinf"
    link.href = "data:text/json;charset=utf-8,"+encodeURIComponent(json_str)
    link.click()

async def prev_result_func(event):
    base=base_lst[0]
    base.reset()

async def next_result_func(event):
    base=base_lst[0]
    base.reset()

async def zoom_in_func(event):
    base=base_lst[0]
    scale=base.scale
    if scale>=0.2:
        scale-=0.1
        if len(event.data)>2:
            base.update_scale(scale,int(event.data[2]),int(event.data[3]))
        else:
            base.update_scale(scale)
        scale=base.scale
        update_scale(f"{base.width}x{base.height} ({round(100/scale)}%)")

async def zoom_out_func(event):
    base=base_lst[0]
    scale=base.scale
    if scale<10:
        scale+=0.1
        console.log(len(event.data))
        if len(event.data)>2:
            base.update_scale(scale,int(event.data[2]),int(event.data[3]))
        else:
            base.update_scale(scale)
        scale=base.scale
        update_scale(f"{base.width}x{base.height} ({round(100/scale)}%)")

async def sync_func(event):
    base=base_lst[0]
    base.sync_to_buffer()
    base.canvas[2].clear()

async def eraser_size_func(event):
    base=base_lst[0]
    eraser_size=min(int(event.data[1]),min(base.selection_size_h,base.selection_size_w))
    eraser_size=max(8,eraser_size)
    base.eraser_size=eraser_size

async def resize_selection_func(event):
    base=base_lst[0]
    cursor=base.cursor
    if len(event.data)>3:
        console.log(event.data)
        base.cursor[0]=int(event.data[1])
        base.cursor[1]=int(event.data[2])
        base.selection_size_w=int(event.data[3])//8*8
        base.selection_size_h=int(event.data[4])//8*8
        base.refine_selection()
        base.draw_selection_box()
    elif len(event.data)>2:
        base.draw_selection_box()
    else:
        base.canvas[-1].clear()
        adjust_selection(cursor[0],cursor[1],base.selection_size_w,base.selection_size_h)

async def eraser_func(event):
    base=base_lst[0]
    if event.data[1]!="eraser":
        base.canvas[-2].clear()
    else:
        x,y=base.mouse_pos
        base.draw_eraser(x,y)

async def resize_func(event):
    base=base_lst[0]
    width=int(event.data[1])
    height=int(event.data[2])
    if width>=256 and height>=256:
        if max(base.selection_size_h,base.selection_size_w)>min(width,height):
            base.selection_size_h=256
            base.selection_size_w=256
        base.resize(width,height)

async def message_func(event):
    if event.data[0]=="click":
        if event.data[1]=="clear":
            await reset_func(event)
        elif event.data[1]=="save":
            await save_func(event)
        elif event.data[1]=="export":
            await export_func(event)
        elif event.data[1]=="accept":
            await commit_func(event)
        elif event.data[1]=="cancel":
            await undo_func(event)
        elif event.data[1]=="zoom_in":
            await zoom_in_func(event)
        elif event.data[1]=="zoom_out":
            await zoom_out_func(event)
        elif event.data[1]=="redo":
            await history_redo_func(event)
        elif event.data[1]=="undo":
            await history_undo_func(event)
        elif event.data[1]=="history":
            await history_setup_func(event)
    elif event.data[0]=="sync":
        await sync_func(event)
    elif event.data[0]=="load":
        await load_func(event)
    elif event.data[0]=="upload":
        await upload_func(event)
    elif event.data[0]=="outpaint":
        await outpaint_func(event)
    elif event.data[0]=="mode":
        if event.data[1]!="selection":
            await sync_func(event)
        await eraser_func(event)
        document.querySelector("#mode").value=event.data[1]
    elif event.data[0]=="transfer":
        await transfer_func(event)
    elif event.data[0]=="setup":
        await draw_canvas_func(event)
    elif event.data[0]=="eraser_size":
        await eraser_size_func(event)
    elif event.data[0]=="resize_selection":
        await resize_selection_func(event)
    elif event.data[0]=="shortcut":
        await setup_shortcut_func(event)
    elif event.data[0]=="resize":
        await resize_func(event)
    
window.addEventListener("message",create_proxy(message_func))

import asyncio

_ = await asyncio.gather(
  setup_func()
)