import dotenv
import uvicorn

dotenv.load_dotenv()

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8080, reload=True)