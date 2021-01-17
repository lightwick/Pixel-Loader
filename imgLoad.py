import os
from typing    import List, Callable
from abc       import ABCMeta, abstractproperty
from tkinter   import Tk, filedialog as TkInter_FileDialog

Tk().withdraw()

class _All_FileTypes:
  name       = "All Files"
  extensions = ["*"]
  file_types = ("All Files", "*.*")
  
class FileGroup:
  All_FileTypes = _All_FileTypes

  def __init__(self, name:str, extensions:List[str]):
    self.name = name
    self.extensions = extensions

  @property
  def file_types(self):
    extensions_string = " ".join([f"*.{x}" for x in self.extensions])
    return (self.name, extensions_string)

class Desktop_FileDialog_Base(metaclass=ABCMeta):

  @abstractproperty
  @property
  def args(self):
    return {}

  def __init__(self,
    show_dialog:       Callable,
    title:             str,
    initial_directory: str,

    file_groups:       List[FileGroup],
  ):
    self.show_dialog       = show_dialog
    self.title             = title
    self.initial_directory = initial_directory

    self.file_groups       = file_groups
    self._validate_initial_directory()

  def show(self):
    path = self.show_dialog(**self.args)
    if(path):
      # self.on_accept(path)
      return path


  def _validate_initial_directory(self):
    if not(self.initial_directory):
      self.initial_directory = os.path.abspath(os.sep)
    else:
      if not(os.path.isdir(self.initial_directory)):
        raise ValueError(f"\n\t_invalid Directory: '{self.initial_directory}'")

class Desktop_FileDialog(Desktop_FileDialog_Base):
  @property
  def args(self):
    return {
      "title":      self.title,
      "initialdir": self.initial_directory,
      "filetypes":  (x.file_types for x in self.file_groups),
    }
  def __init__(self,
    title:             str,
    initial_directory: str,
    file_groups:       List[FileGroup],
  ):
    super().__init__(
      show_dialog       = TkInter_FileDialog.askopenfilename,
      title             = title,
      initial_directory = initial_directory,
      file_groups       = file_groups,
    )

'''
    def __init__(self):
        b = Desktop_FileDialog(
                title             = "Select File",
                initial_directory = "",
                file_groups = [
                    FileGroup(name="Image Files", extensions=["jpg", "jpeg", "png", "gif"]),
                    FileGroup.All_FileTypes,
                ],
            ).show()
        print(b)
'''
