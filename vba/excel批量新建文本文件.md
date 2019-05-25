## 根据excel批量新建包含不同内容的文本文件

```vb
Public Sub CommandButton1_Click()
    For i = 1 To ActiveSheet.UsedRange.rows.Count:
        CreateFile (i)
    Next
End Sub


Public Function CreateFile(ByVal index)
    Dim gPath As String
    Dim sFile As Object, Fso As Object

    gPath = Application.ActiveWorkbook.Path
    Set Fso = CreateObject("Scripting.FileSystemObject")
    Set sFile = Fso.CreateTextFile(gPath & "/" & Cells(index, "A").Value & ".bat", True)
    sFile.WriteLine (Cells(index, "B").Value)
    sFile.WriteLine (Cells(index, "C").Value)
    sFile.Close
    Set sFile = Nothing
    Set Fso = Nothing
End Function
```
