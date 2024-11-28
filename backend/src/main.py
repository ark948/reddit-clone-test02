from fastapi import FastAPI





app = FastAPI()







@app.get('/test')
async def test_route():
    return {"message": "test successful"}