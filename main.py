import uvicorn
from fastapi import FastAPI, File, UploadFile, Form, status, HTTPException, Response
from io import BytesIO
import towhee
import utils
from starlette.responses import StreamingResponse


app = FastAPI()

@app.get('/')
def hello():
    return {'text': 'hello world'}

@app.post("/api/trans")
async def transform_api(file: UploadFile = File(...), model_name: str = Form(...)):
    extension = file.filename.split(".")[-1].lower() in ("jpg", "jpeg", "png")
    if not extension:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                        detail=f'File {file.filename} should be jpg, jpeg or png')

    if model_name.lower() not in ['celeba', 'facepaintv1', 'facepaitv2', 'hayao', 'paprika', 'shinkai']:
        return f"Specified Model: {model_name} Name Does not exist"
    
    input_image = utils.read_image(file.file.read())
    file.file.close()
    output_image = utils.translate_image(input_image, model_name)
    return {'image': BytesIO(output_image.tobytes())}

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8080, debug = True)