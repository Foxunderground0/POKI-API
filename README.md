# Pokimane Twitter Image Emotion Classification

This project is a tribute to Pokimane, a popular content creator on Twitter. The goal of this project is to scrape images from Pokimane's Twitter account, classify the emotions in those images, and serve them through a Node.js server.

![Display](/Immages/PokiAPI.gif)

## Repository Structure

The repository has the following structure:

-   `.gitignore`
-   `Emotion Classifier/`
    -   `emotions.py`
    -   `model.h5`
-   `File Hasher/`
    -   `hash_filenames.py`
    -   `scraped_duplicate_remover.py`
-   `Node/`
    -   `index.js`
    -   `package.json`
-   `Scraper/`
    -   `twitter_scraper.py`
-   `LICENSE`
-   `Immages/`
    -   `scraped/`
    -   `to_sort/`
    -   `sorted/`
    -   `display/`

## Functionality

The repository consists of several scripts that perform specific tasks:

1. The `twitter_scraper.py` script is used to scrape tweets from Pokimane's Twitter account. The scraped images are stored in the `/Images/scraped` directory.

2. The scraped images are then transferred from the `/Images/scraped` directory to the `/Images/to_sort` directory.

3. The `scraped_duplicate_remover.py` script is run to remove any duplicate images in the `/Images/to_sort` directory. It uses a sha256 hash of the images to compare and identify duplicates.

4. The `emotions.py` script is used to classify the emotions in the images. It utilizes a CNN model trained on emotion detection. The script uses face recognition to locate faces in the images, extracts the pixels within those coordinates, resizes them to 48x48 pixels, and passes them through the trained model. The emotions detected are then appended to the filenames of the sorted images in the `/Images/sorted` directory.

5. The `hash_filenames.py` script generates SHA256 hashes for the filenames in the `/Images/sorted` directory. The hashed filenames are saved in the format `[emotion]_[sha256hash].jpg`.

6. The Node.js server is started by running the `index.js` file in the `Node` directory. The server serves the processed images located in the `/Images/display` directory. It uses Express.js and provides endpoints to access the images.

## Usage

To use this repository, follow these steps:

1. Set up the environment by installing the required dependencies. You can find the dependencies in the `package.json` file in the Node directory.

2. Run the `Scraper/twitter_scraper.py` script to scrape tweets from Pokimane's Twitter account and store the images in the `/Images/scraped` directory.

3. Transfer the scraped images from the `/Images/scraped` directory to the `/Images/to_sort` directory.

4. Run the `File Hasher/scraped_duplicate_remover.py` script to remove any duplicate images in the `/Images/to_sort` directory.

5. Run the `Emotion Classifier/emotions.py` script to classify the emotions in the images using the trained model (`Emotion Classifier/model.h5`). The emotions will be appended to the filenames of the sorted images in the `/Images/sorted` directory.

6. Run the `File Hasher/hash_filenames.py` script to generate SHA256 hashes for the filenames in the `/Images/sorted` directory. The hashed filenames will be saved in the format `[emotion]_[sha256hash].jpg`.

7. Start the Node.js server by running the `Node/index.js` file. The server will serve the processed images located in the `/Images/display` directory.

8. Access the served images through the server's endpoint, e.g., `http://localhost:8081/`.

Please note that you may need to adjust the paths and configurations in the scripts according to your system setup.

## License

This project is licensed under the [MIT License](LICENSE).
