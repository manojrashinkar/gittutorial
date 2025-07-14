// netlify/functions/visitorCount.js
const fs = require('fs');
const path = require('path');

const filePath = path.resolve('/tmp/visitorCount.json');

exports.handler = async function (event, context) {
  try {
    let count = 0;

    // Read existing count
    if (fs.existsSync(filePath)) {
      const data = fs.readFileSync(filePath, 'utf-8');
      count = JSON.parse(data).count || 0;
    }

    // Increment count
    count++;

    // Write updated count
    fs.writeFileSync(filePath, JSON.stringify({ count }), 'utf-8');

    return {
      statusCode: 200,
      body: JSON.stringify({ count }),
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      }
    };
  } catch (err) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Failed to process count', details: err.message }),
    };
  }
};
