const fs = require('fs')

function respondWithDocument(event) {
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

function respondWithStyles() {
    const document = fs.readFileSync("document.css", "utf8")
    const response = {
        statusCode: 200,
        headers: {
            "content-type": "text/css"
        },
        body: document,
    }
    return response
}

function queryStringParameter(event, parameter) {
    if (event.queryStringParameters) {
        return event.queryStringParameters[parameter]
    } else {
        return null
    }
}

exports.handler = async (event) => {
    if (queryStringParameter(event, "resource") == "css") {
        return respondWithStyles()
    }
    return respondWithDocument(event)
}
