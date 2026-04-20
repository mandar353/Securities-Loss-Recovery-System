from pathlib import Path
from io import BytesIO
import asyncio
import shutil
from fastapi import UploadFile
from app.services.twitter_logic import calculate_twitter_loss
from app.services.kraft_logic import calculate_kraft_loss
from app.services.loss_calculator import process_file

def test_twitter_loss():
    row = {"purchases": 100, "sales": 80, "holdings": 10, "transaction type": "sale"}
    loss = calculate_twitter_loss(row)
    assert loss == 20

def test_kraft_loss():
    row = {"purchase_price": 50, "sale_price": 60, "quantity": 5}
    loss = calculate_kraft_loss(row)
    assert loss == 0

def test_process_file_with_sample_workbook():
    sample_path = Path("data/input/sample_data.xlsx")
    output_dir = Path("data/test_output")
    if output_dir.exists():
        shutil.rmtree(output_dir)

    with sample_path.open("rb") as file_handle:
        upload = UploadFile(filename=sample_path.name, file=BytesIO(file_handle.read()))

    result = asyncio.run(process_file(upload, output_dir=output_dir))

    assert result["message"] == "Processed successfully"
    assert result["total_recognized_loss"] == 50.0
    assert (output_dir / result["output_filename"]).exists()

if __name__ == "__main__":
    test_twitter_loss()
    test_kraft_loss()
    print("All tests passed!")
