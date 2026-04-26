from app.app import create_app

app = create_app('production')

# For Vercel serverless environment
if __name__ == '__main__':
    app.run()
