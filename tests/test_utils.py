import tempfile
import os
from app.utils.data_loader import load_and_embed_files

# Validate FAISS embedding and metadata
def test_load_and_embed_files_txt():
    # Create a temporary text file with some content
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w") as tmp:
        tmp.write("Test content for vectorstore.")
        tmp_path = tmp.name

    try:
        # Run the loader
        vectorstore = load_and_embed_files([tmp_path])

        # Search with a simple query
        results = vectorstore.similarity_search("Test", k=1)

        assert len(results) == 1
        doc = results[0]

        assert "Test content" in doc.page_content
        assert doc.metadata.get("source") == "user_uploaded"
        assert "file_name" in doc.metadata

    finally:
        os.remove(tmp_path)  # Clean up the temp file
