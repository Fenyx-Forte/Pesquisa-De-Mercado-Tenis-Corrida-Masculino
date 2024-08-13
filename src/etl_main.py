import etl_app

if __name__ == "__main__":
    etl_app.configurar_loguru()
    etl_app.configurar_polars()
    etl_app.pipeline()
