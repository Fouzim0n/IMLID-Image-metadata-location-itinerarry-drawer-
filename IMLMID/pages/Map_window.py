import tkinter as tk
from PIL import Image, ImageTk # optional imports that might come useful later
from utils import Theme
from tkintermapview import TkinterMapView

from metadata_extractor import process_all_images

theme = Theme()
styles = theme.tk_styles()



class Map_window(tk.Toplevel):
    def create(self,fileList):

        # optional ui code which i don't understand. (might be useful later)
        """ 
        # Variables to store original image and references
        self.original_image = None
        self.bg_photo = None
        self.bg_label = None
        self.last_width = None
        self.last_height = None
        
        # Load background image
        try:
            self.original_image = Image.open("assets/photo-location.webp")  
        except Exception as e:
            print(f"Error loading image: {e}")
        
        # Create background label
        window.bg_label = tk.Label(window)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        """
        
        # create the map 
        map= TkinterMapView(self, width=800, height=600, corner_radius=0)
        map.set_position(36.7538, 3.0588)  # makes the map open on algiers by default 
        map.set_zoom(9) #makes the map open without being zoomed too much

        # compiles the metadata of all files in one list then compiles only gps data and put it in it's own list
        metadata_list= process_all_images(fileList)
        gps_data= [item["location"] for item in metadata_list] 
        
        if (gps_data):
            locations= [] 
            for item in gps_data: # this loop converts gps data from strings into usuable list formats which will be stored in the locations list (basically: a list of lists[2])
                if (not item):
                    continue  # skip images with no GPS
                try:
                    location= [float(x) for x in item.split(',') ]
                    locations.append(location)
                except Exception as e:
                    print(f"Skipping invalid GPS data: {item} ({e})")
        
            # set a pin at every valid location
            for i, location in enumerate(locations):
                map.set_marker(location[0], location[1], text=f"Location {i+1}")    

            # draw the itenerary after making sure there are more than 2 locations
            if(len(locations)>=2): 
                map.set_path(locations) 

        map.pack(fill="both", expand=True) #pack the map

        # the button that colses the map
        button = tk.Button(self, text="Close", 
                          command=lambda: self.destroy())
        button.config(**styles["primary_button"])
        button.pack()
        
        #follow up for the previous ui code i couldn't understand (might come useful later)
    """   
        # Bind resize event
        self.bind("<Configure>", self.on_window_resize)
   
    def on_window_resize(self, event):
        #Update background image only when size actually changes
        if self.original_image and (self.last_width != event.width or self.last_height != event.height):
            self.last_width = event.width
            self.last_height = event.height
            
            try:
                resized_image = self.original_image.resize((event.width, event.height))
                self.bg_photo = ImageTk.PhotoImage(resized_image)
                self.bg_label.config(image=self.bg_photo)
                self.bg_label.image = self.bg_photo
            except Exception as e:
                print(f"Error resizing image: {e}")
    """