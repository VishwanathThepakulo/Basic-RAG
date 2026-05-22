from ingestion import db_ingestion






def main():
    print("Hello from basic-rag!")
    user_pdf_input = input("Enter a pdf path : ")
    user_pdf_output = db_ingestion.pdf_loader(user_pdf_input)
    for para in user_pdf_output:
        print("PARAGRAPH:")
        print(para)
        print("="*50)

if __name__ == "__main__":
    main()
