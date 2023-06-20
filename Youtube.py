import os
import tkinter as tk
from tkinter import NW, filedialog
import pytube
from moviepy.audio.io.AudioFileClip import AudioFileClip

Shrift_20 = "Helvetica 20 bold"
Shrift_14 = "Helvetica 14 bold"
Shrift_9 = "Helvetica 9 bold"
Shrift_11 = "Helvetica 11 bold"
Shrift_10 = "Helvetica 10 bold"


# Функция для выбора папки загрузки
def select_download_folder():
    download_folder_path = filedialog.askdirectory()
    entry_down.delete(0, tk.END)
    entry_down.insert(0, download_folder_path)


# Функция конвертации из mp4 в mp3
def convert_mp4_to_mp3():
    try:
        # Получение пути к видеофайлам для конвертации
        video_file_paths = filedialog.askopenfilenames(title="Выберите видеофайлы для конвертации...",
                                                       filetypes=(("Video files", "*.mp4"),))

        if len(video_file_paths) == 0:
            views_label_danger.config(text="Выберите файлы для конвертации", fg="red", font=Shrift_11)
            return

        for i, video_file_path in enumerate(video_file_paths, 1):
            # Получение пути для сохранения аудиофайла
            audio_file_path = os.path.splitext(video_file_path)[0] + ".mp3"

            # Создание AudioFileClip из исходного видеофайла
            clip = AudioFileClip(video_file_path)

            # Конвертация в аудиофайл формата mp3
            clip.write_audiofile(audio_file_path, bitrate=selected_bitrate.get())

            # Закрытие объекта AudioFileClip
            clip.close()

        # Вывод списка файлов
        views_label.config(text="Конвертация завершена\n "
                                f"Качество звука: {selected_bitrate.get()}\n",
                           fg="red", font=Shrift_11)

    except Exception as e:
        print(e)
        views_label_danger.config(text="Ошибка конвертации. \n"
                                       "Нажмите Clear info", fg="red", font=Shrift_9)


# Информация о видео и аудио в максимально загружаемом формате
def max_format_video_audio():
    try:
        clear_info()
        link = entry_url.get()
        ds = pytube.YouTube(link)
        m_video = ds.streams.get_highest_resolution()
        m_audio = ds.streams.get_audio_only()
        views_label.config(text=f" {m_video.title[:34]} \n "
                                f" {ds.author[:34]}\n"
                                f"Видео: {m_video.resolution}, {m_video.abr}, {m_video.mime_type} \n "
                                f"Размер видео в mp4:  {round(m_video.filesize / 1024000, 2)} Mb \n"
                                f"Качество аудио: {m_audio.abr}, {m_audio.mime_type} \n"
                                f"Размер аудио в mp4:  {round(m_audio.filesize / 1024000, 2)} Mb \n"
                                f' {ds.length // 3600}'
                                f" часов {ds.length % 3600 // 60} минут {ds.length % 60} секунд",
                           fg="red", font=Shrift_10)
    except:
        views_label_danger.config(text="Введите URL для информации \n"
                                       "Нажмите Clear info", fg="red", font=Shrift_11)


def download_video():
    try:
        link = entry_url.get()
        save_path = entry_down.get()
        clear_info()
        if save_path == "":
            return views_label_danger.config(text="Некорректный путь загрузки \n"
                                                  "Нажмите Clear info", fg="red", font=Shrift_11)
        yt = pytube.YouTube(link)
        stream = yt.streams.get_highest_resolution()  # метод максимального качества
        stream.download(save_path)

        views_label.config(text=f" {stream.title[:34]} \n "
                                f"Качество видео: {stream.resolution}, {stream.abr}, {stream.mime_type} \n "
                                f" {yt.length // 3600} часов {yt.length % 3600 // 60} минут"
                                f" {yt.length % 60} секунд  \n"
                                f"кодек {stream.codecs} \n"
                                f"размер файла {round(stream.filesize / 1024000, 2)} Mb \n"
                                f"Видео успешно СКАЧАНО",

                           fg="red", font=Shrift_10)
    except:
        views_label_danger.config(text="Не корректный URL или путь \n"
                                       "Нажмите Clear info", fg="red", font=Shrift_11)


def download_audio():
    try:
        link = entry_url.get()
        save_path = entry_down.get()
        clear_info()
        if save_path == "":
            return views_label_danger.config(text="Некорректный путь загрузки \n"
                                                  "Нажмите Clear info", fg="red", font=Shrift_11)
        yt = pytube.YouTube(link)
        stream = yt.streams.get_audio_only()
        stream.download(save_path)

        views_label.config(text=f" {stream.title[:34]} \n "
                                f"Качество аудио: {stream.abr}, {stream.mime_type} \n "
                                f"{yt.length // 3600} часов {yt.length % 3600 // 60} минут"
                                f" {yt.length % 60} секунд  \n"
                                f"кодек {stream.codecs} \n"
                                f"размер файла {round(stream.filesize / 1024000, 2)} Mb \n"
                                f"Аудио успешно СКАЧАНО",
                           fg="red", font=Shrift_10)
    except:
        views_label_danger.config(text="Не корректный URL или путь \n"
                                       "Нажмите Clear info", fg="red", font=Shrift_11)


# Функция для очистки url
def clear_url():
    entry_url.delete(0, tk.END)


def clear_info():
    views_label.config(text="")
    views_label_danger.config(text="")


root = tk.Tk()

root.geometry("512x512")
root.maxsize(width=530, height=530)
root.minsize(width=512, height=512)
root.title("Загрузчик видео/аудио с Youtube. Конвертер MP4/MP3")

#  Создание объекта Canvas
canvas = tk.Canvas(root, width=512, height=512)
canvas.pack()

# Загрузка изображения
image = tk.PhotoImage(file="copy.png")
# Создание изображения на заднем плане
canvas.create_image(0, 0, anchor=NW, image=image)

# Add a text in canvas для URL
canvas.create_text(100, 30, text="Введите URL", fill="red",
                   font=Shrift_20)

# Создание Entry для URL
entry_url = tk.Entry(canvas, font=Shrift_14)

# Размещение Entry над изображением в Canvas для URL
canvas.create_window(350, 30, window=entry_url, width=300, height=28)

# Создание кнопки для выбора папки загрузки
download_folder_button = tk.Button(root, text="Выбрать папку загрузки",
                                   command=select_download_folder,
                                   width=23, height=1)
download_folder_button.configure(fg="red", bg="black", font=Shrift_9)
download_folder_button.place(x=12, y=63)

# Создание Entry для папка загрузки
entry_down = tk.Entry(canvas, font=Shrift_14)

# Размещение Entry над изображением в Canvas для папка загрузки
canvas.create_window(350, 75, window=entry_down, width=300, height=28)

# Создание кнопки для информации
info_button = tk.Button(root, text="Информация о ВИДЕО",
                        command=max_format_video_audio,
                        width=23, height=2)
info_button.configure(fg="red", bg="black", font=Shrift_11)
info_button.place(x=11, y=135)
#
# Создание лэйбла для вывода информации видео/аудио
views_label = tk.Label(root)
views_label.place(x=230, y=102)

# Создание лэйбла для вывода информации предупреждений
views_label_danger = tk.Label(root)
views_label_danger.place(x=235, y=269)

# Создание кнопки для скачивания видео
download_video_button = tk.Button(root, text="Скачать видео", command=download_video,
                                  font=Shrift_11, width=14, height=1, bg='deep sky blue')
download_video_button.place(x=22, y=192)

# Создание кнопки для скачивания аудио
download_audio_button = tk.Button(root, text="Скачать аудио", command=download_audio,
                                  font=Shrift_11, width=14, height=1, bg='deep sky blue')
download_audio_button.place(x=22, y=230)

# Создание кнопки для скачивания аудио и конвертации в mp3
download_audio_button = tk.Button(root, text="MP4 to MP3", command=convert_mp4_to_mp3,
                                  font=Shrift_11, width=14, height=1, bg='deep sky blue')
download_audio_button.place(x=22, y=269)

# Диалоговое окно выбора битрейта
bitrate_options = ["96k", "128k", "192k", "256k", "320k"]
selected_bitrate = tk.StringVar(value="128k")
bitrate_menu = tk.OptionMenu(root, selected_bitrate, *bitrate_options)  # добавление выпадающего списка
bitrate_menu.config(font=Shrift_9, bg='deep sky blue')
bitrate_menu.place(x=160, y=269)

# Создание кнопки для очистки url
clear_url_button = tk.Button(root, text="Clear URL", command=clear_url,
                             font=Shrift_11, width=14, height=1, bg='deep sky blue')
clear_url_button.place(x=191, y=230)

# Создание кнопки для очистки Информации о Видео
clear_url_button = tk.Button(root, text="Clear info", command=clear_info,
                             font=Shrift_11, width=14, height=1, bg='deep sky blue')
clear_url_button.place(x=360, y=230)


# Создаем инфо для других форматов видео и аудио
def info_down():
    clear_info()
    views_label.config(text="Файл УСПЕШНО СКАЧАН \n"
                            "Нажмите Clear info", fg="red", font=Shrift_11)


button = None
video_listbox = None


# Функция для создания списка и кнопки для дополнительного скачивания Видео/Аудио в разных форматах
def creat_dop():
    try:
        link = entry_url.get()
        ds = pytube.YouTube(link)
        clear_info()

    except:
        views_label_danger.config(text="Введите URL для информации \n"
                                       "Нажмите Clear info", fg="red", font=Shrift_11)
    info_video = []

    for stream in ds.streams.filter(progressive=True):
        info_video.append(
            f'Формат: {stream.mime_type}, {stream.abr} , {stream.resolution} '
            f"Размер:  {round(stream.filesize / 1024000, 2)} Mb , "
            f'тэг: {stream.itag}')

    for stream in ds.streams.filter(type="audio"):
        if int(stream.abr[:-4]) >= 90:
            info_video.append(
                f'АУДИО: {stream.mime_type},  {stream.abr}, '
                f"Размер:  {round(stream.filesize / 1024000, 2)} Mb , "
                f'тэг: {stream.itag}')

    for stream in ds.streams.filter(type="video"):
        if int(stream.resolution[:-1]) >= 720:
            info_video.append(
                f'ВИДЕО БЕЗ ЗВУКА: {stream.mime_type},  {stream.resolution},  '
                f"Размер:  {round(stream.filesize / 1024000, 2)} Mb , "
                f' тэг: {stream.itag}')

    # Это сделано для удаления предыдущего листбокса и создание нового списка
    global video_listbox
    if video_listbox:
        video_listbox.destroy()
        video_listbox = None

    video_listbox = tk.Listbox(font=Shrift_9,
                               bg="blue", height=5, width=65)
    for file in info_video:
        video_listbox.insert(tk.END, file)
    video_listbox.place(x=21, y=370)

    # Создаем полосу прокрутки для списка файлов
    scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL)
    scrollbar.place(x=480, y=370)
    video_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=video_listbox.yview)

    # # Создание Расширенных возможностей
    def download_video_po_vibor():
        link = entry_url.get()
        save_path = entry_down.get()
        if save_path == "":
            return views_label_danger.config(text="Некорректный путь загрузки \n"
                                                  "Нажмите Clear info", fg="red", font=Shrift_11)
        index = video_listbox.curselection()
        tag = video_listbox.get(index)
        yt = pytube.YouTube(link)
        stream = yt.streams.get_by_itag(tag[-3:])
        stream.download(save_path)
        info_down()

    # Это сделано для удаления предыдущей кнопки и создание новой. Чтобы была не нарушена ирархия листбока и кнопки
    global button
    if button:
        button.destroy()
        button = None

    button = tk.Button(root, text="Скачать по выбору", command=download_video_po_vibor,
                       font=Shrift_11, width=40, height=1, bg='deep sky blue')
    button.place(x=80, y=465)


# Создание кнопки для  "Качество видео/аудио на выбор:"
creat_dop_button = tk.Button(canvas, text="Качество видео/аудио на выбор:", command=creat_dop,
                             font=Shrift_11, width=40, height=1, bg='deep sky blue')
creat_dop_button.place(x=80, y=330)

root.mainloop()
