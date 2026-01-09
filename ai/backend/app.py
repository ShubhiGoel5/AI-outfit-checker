import base64
import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
from prompt import SYSTEM_PROMPT, USER_PROMPT

load_dotenv()

client = OpenAI()

app = FastAPI(title="AI Fitcheck System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def encode_image(image: UploadFile) -> str:
    return base64.b64encode(image.file.read()).decode("utf-8")

@app.post("/fitcheck")
async def fitcheck(image: UploadFile = File(...)):
    if image.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Unsupported image format")

    image_b64 = encode_image(image)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": USER_PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_b64}"
                        },
                    },
                ],
            },
        ],
    )

    raw = response.choices[0].message.content

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON returned by model")

    return parsed
