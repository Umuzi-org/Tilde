export const getPrColor = (oldestOpenPrTime) => {
    const now = new Date()
    const milliseconds = 1000 * 60 * 60 * 24
    // console.log(now)
    console.log("oldestOpenPrTime: ", typeof(new Date(oldestOpenPrTime)), oldestOpenPrTime)

    const timeDifferenceInSeconds = Math.abs(now - new Date(oldestOpenPrTime))
    const timeDifferenceInDays = Math.ceil(timeDifferenceInSeconds / milliseconds)
    // console.log(timeDifferenceInDays)

    let prColor

    if(timeDifferenceInDays <= 2) {
        prColor = "orange"
    }else {
        prColor = "red"
    }

    return prColor 
}

export const getTildeReviewColor = (openPrTime) => {
    const now = new Date()
    const milliseconds = 1000 * 60 * 60 * 24
    console.log("openPrTime: ", typeof(new Date(openPrTime)), openPrTime)
    const timeDifferenceInSeconds = Math.abs(now - new Date(openPrTime))
    console.log("time difference in seconds: ", timeDifferenceInSeconds)
    const timeDifferenceInDays = Math.ceil(timeDifferenceInSeconds / milliseconds)
    console.log("time difference in days: ", timeDifferenceInDays)

    let tildeColor

    if(timeDifferenceInDays <= 3) {
        tildeColor = "orange"
    }else {
        tildeColor = "red"
    }

    return tildeColor 
}