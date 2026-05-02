from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from services.ocr import extract_text
from services.gemini import analyze_text

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        allowed_types = [
            "application/pdf",
            "image/jpeg",
            "image/png",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ]

        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        contents = await file.read()

        if not contents:
            raise HTTPException(status_code=400, detail="Empty file")

        text = await extract_text(file, contents)

        if not text or len(text.strip()) < 10:
            raise HTTPException(
                status_code=400, detail="Could not extract meaningful text"
            )

        result = await analyze_text(text)

        return JSONResponse(content={"success": True, "data": result})

    except HTTPException as e:
        raise e

    except Exception as e:
        return JSONResponse(
            status_code=500, content={"success": False, "error": str(e)}
        )
