import json
from PIL import Image
import time
import statistics
import logging


def handler(event, context):
    benchmark()
    return {
        'statusCode': 200,
        'body': json.dumps('image Processing Completed ')
    }


def image_processing():
    """
    This method resizes the image.
    :return: image
    """
    image_to_process = Image.open("image.jpg")

    # Resize the image
    resized_image = image_to_process.resize((1024, 1000))

    return resized_image


def benchmark():
    """
    This is the main benchmarking method that runs the function and calculates the throughput and the average time
    :return: None
    """
    throughput_time = {"Image": []}
    average_duration_time = {"Image": []}
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    for i in range(40):  # adjust accordingly so whole thing takes a few sec
        logger.info('Image Processing execution beginning')
        t0 = time.time()
        image_processing()
        t1 = time.time()
        logger.info('Image Processing function ended, calculating metrics')
        if i >= 20:  # We let it warmup for first 20 rounds, then consider the last 20 metrics
            throughput_time["Image"].append(1 / ((t1 - t0) * 1000))
            average_duration_time["Image"].append(((t1 - t0) * 1000) / 1)

    # Printing out results for throughput
    for name, numbers in throughput_time.items():
        logger.info("The throughput time")
        length = str(len(numbers))
        median = str(statistics.median(numbers))
        mean = str(statistics.mean(numbers))
        stdev = str(statistics.stdev(numbers))
        output = "FUNCTION {} used {} times. > MEDIAN {} ops/ms > MEAN {} ops/ms  > STDEV {} ops/ms".format(name,
                                                                                                            length,
                                                                                                            median,
                                                                                                            mean,
                                                                                                            stdev)
        logger.info(output)

    # printing out results for average duration
    for name, numbers in average_duration_time.items():
        logger.info("The average Duration details")
        length = str(len(numbers))
        median = str(statistics.median(numbers))
        mean = str(statistics.mean(numbers))
        stdev = str(statistics.stdev(numbers))
        output = "FUNCTION {} used {} times. > MEDIAN {} ms/ops > MEAN {} ms/ops  > STDEV {} ms/ops".format(name,
                                                                                                            length,
                                                                                                            median,
                                                                                                            mean,
                                                                                                            stdev)
        logger.info(output)

    logger.critical("The benchmark is finished properly")

