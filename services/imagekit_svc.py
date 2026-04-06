from imagekitio import ImageKit
import os


class ImageKitService:
    def __init__(self):
        self.imageKit = ImageKit( 
            private_key=os.getenv("IMAGEKIT_PRIVATE_KEY")
        )

    def upload_image(self, file):
        print("We are in the imageKitIo function")
        try:
            upload = self.imageKit.files.upload(
                file = file.read(),
                file_name = file.filename
            )
            print(upload.url)
            return upload.url
        except Exception as e:
            print("File upload failed:", e)

    

imageKit_service = ImageKitService()