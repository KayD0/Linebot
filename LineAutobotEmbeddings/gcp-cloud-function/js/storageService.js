const { Storage } = require('@google-cloud/storage');

class StorageService {
  constructor() {
    this.storage = new Storage();
  }

  /**
   * Writes a JSON object to a file in Google Cloud Storage
   * @param {string} bucketName - The name of the GCS bucket.
   * @param {string} path - The path to the directory where the file will be stored.
   * @param {string} fileName - The name of the file to be written.
   * @param {Object} data - The JSON object to write.
   * @returns {Promise<void>}
   */
  async writeJsonToFile(bucketName, path, fileName, data) {
    try {
      const fullPath = `${path}/${fileName}`;
      const file = this.storage.bucket(bucketName).file(fullPath);
      const jsonData = JSON.stringify(data, null, 2);
      await file.save(jsonData);
      console.log(`File ${fullPath} written to bucket ${bucketName}.`);
    } catch (error) {
      console.error('Error writing file:', error);
      throw new Error('Error writing JSON file');
    }
  }
}

module.exports = StorageService;