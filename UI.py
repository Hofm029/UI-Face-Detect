import cv2
import os
from PIL import Image, ImageTk
from tkinter import filedialog
from alig import function_2,haar
import customtkinter as tk
class Camera:
    def __init__(self, canvas, width, height):
        self.save_folder = "captured_images"
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)
        self.count=1
        self.canvas = canvas
        self.width = width
        self.height = height
        self.is_camera_on = False
        self.current_frame = None
        self.cap = cv2.VideoCapture()
    def update_frame(self):
        ret, frame = self.cap.read()
        frame = haar(frame)
        if ret:
            self.current_frame  = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.current_frame  = Image.fromarray(self.current_frame )
            self.current_frame  = self.current_frame .resize((self.width, self.height))
            photo = ImageTk.PhotoImage(self.current_frame)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.image = photo
        self.canvas.after(10, self.update_frame)
    def toggle_camera(self):
        self.is_camera_on = not self.is_camera_on
        if self.is_camera_on == True:
            self.cap = cv2.VideoCapture(0)
        elif self.is_camera_on == False:
            self.cap.release()
        print(self.is_camera_on)
    def start(self):
        self.update_frame()
    def capture(self):
        if self.current_frame is not None:
            img = self.current_frame
            image_path = os.path.join(self.save_folder,  f"image_{self.count}.jpg")
            img.save(image_path)
            self.count +=1
    def restart_folder(self):
        os.makedirs(self.save_folder)
def change_canvas():
    global current_canvas
    # Ẩn canvas hiện tại
    current_canvas.place_forget()

    # Thay đổi giữa canvas1 và canvas2
    if current_canvas == main_canvas:
        current_canvas = camera_canvas
    else:
        current_canvas = main_canvas

    current_canvas.place(x=350, y=30)
def open_image2():
    global file_path2
    # Mở hộp thoại để chọn tệp hình ảnh
    file_path2 = filedialog.askopenfilename(initialdir="./", title="Select Image", filetypes=(("Image Files", "*.jpg *.png"),))
    # Kiểm tra xem người dùng đã chọn một tệp hình ảnh hay chưa
    if file_path2:
        image_sourc = Image.open(file_path2)
        image = image_sourc.resize((220, 160))
        photo = ImageTk.PhotoImage(image)
        canvas_img2.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas_img2.image = photo
def button_2():
    global  file_path2
    img = cv2.imread(file_path2)
    img = function_2(img)
    img = Image.fromarray(img)
    img = img.resize((700,500))
    img = ImageTk.PhotoImage(img)
    # Hiển thị hình ảnh lên Canvas
    main_canvas.create_image(0, 0, anchor=tk.NW, image=img)
    main_canvas.image = img


def combine_command():
    change_canvas()
    camera.toggle_camera()

window = tk.CTk()
window.geometry('1200x500')
tk.set_default_color_theme("dark-blue")
# Tạo một Canvas trong Frame để hiển thị hình ảnh từ camera
main_canvas = tk.CTkCanvas(window, width=630, height=475)
camera_canvas = tk.CTkCanvas(window, width=630, height=475)
current_canvas = main_canvas
#current_canvas.place(relx=0.45, rely=0.35, anchor=tk.CENTER)
current_canvas.place(x=350, y=30)
camera = Camera(camera_canvas, width=630, height=475)
camera.start()
button_texts = ["Detect"]
button_commands = [button_2]
#Tạo một Frame để chứa ba nút
frame_buttons = tk.CTkFrame(window)
frame_buttons.pack(side=tk.LEFT, padx=20)

# Tạo ba nút trong Frame
button_change = tk.CTkButton(master=window,
                                 width=120,
                                 height=32,
                                 border_width=0,
                                 corner_radius=8,
                                 text="Change",
                                 command=combine_command)
button_change.place(x=25, y=100)
for text, command in zip(button_texts, button_commands):

    button = tk.CTkButton(master=frame_buttons,
                                 width=120,
                                 height=32,
                                 border_width=0,
                                 corner_radius=8,
                                 text=text,
                                 command=command)
    button.pack()
window.bind('<space>', lambda event: camera.capture())

# Tạo một nút để mở hình ảnh
button_open_image2 = tk.CTkButton(master=window,
                                 width=120,
                                 height=32,
                                 border_width=0,
                                 corner_radius=8,
                                 text="Open Image",
                                 command=open_image2)
button_open_image2.place(x=960, y=200)

button_capture = tk.CTkButton(master=window,
                                 width=120,
                                 height=32,
                                 border_width=0,
                                 corner_radius=8,
                                 text="Capture",
                                 command=camera.capture)
button_capture.place(x=960, y=100)

# Tạo một Canvas để hiển thị hình ảnh (canvas_img1)
canvas_img2 = tk.CTkCanvas(window, width=220, height=160)
canvas_img2.place(x=1160, y=340)


posx_slide = 0.1
posy_slide = 0.18

window.mainloop()

# Giải phóng tài nguyên
camera.cap.release()
cv2.destroyAllWindows()
