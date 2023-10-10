from django.db import models
from django.contrib.auth.models import User

class FolderDetail(models.Model):
    foldername = models.CharField(max_length=50)
    folderuser = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.foldername
    
    class Meta:
        db_table = 'folder_detail'

class FileDetail(models.Model):
    filetitle = models.CharField(max_length=50)
    folder = models.ForeignKey(FolderDetail,on_delete=models.CASCADE)
    file = models.FileField(upload_to="Files")

    def __str__(self):
      return self.filetitle
    
    class Meta:
        db_table = 'file_detail'

