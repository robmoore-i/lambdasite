const fs = require('fs')

exports.handler = async (event) => {
    const document = fs.readFileSync("document.html", "utf8")
    const response = {
        statusCode: 200,
        headers: {
            "content-type": "text/html"
        },
        body: document,
    }
    return response
}
