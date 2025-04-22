@echo off
setlocal

set "filename=1"
set "filetxt=%filename%.txt"
set "filebat=%filename%.bat"

:: لو الملف بصيغة .txt موجود
if exist "%filetxt%" (

    ren "%filetxt%" "%filename%.bat"
    goto end
)

:: لو الملف بصيغة .bat موجود
if exist "%filebat%" (

    ren "%filebat%" "%filename%.txt"
    goto end
)



:end
