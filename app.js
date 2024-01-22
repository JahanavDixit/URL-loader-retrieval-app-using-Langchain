const axios = require('axios');
const fs = require('fs');
const apiUrl = 'http://127.0.0.1:5000/ask'; // Update this with your actual API endpoint

const requestData = {
  prompt: 'Hello tell me about this website', // Replace this with your actual prompt
};

axios.post(apiUrl, requestData)
  .then(response => {
    //fs.writeFileSync('./a.txt', response.data);
    console.log('Response:', response.data);
  })
  .catch(error => {
    console.error('Error:', error.message);
  });
