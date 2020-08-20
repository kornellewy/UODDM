class FoldersNamesError(Exception):
    """
    Exeption trow then format of image and annotaion format are wrong definde.
    Method and atibutes are rly clear named so no coments on that.
    """
    def __init__(self, images_folder_name, annotations_folder_name,\
         message="Folder names was not in predeifne folders names like :."):
        self.images_folder_name = images_folder_name
        self.annotations_folder_name = annotations_folder_name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} {self.images_folder_name} or {self.annotations_folder_name}'
