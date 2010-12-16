function (key, values, rereduce) {
    /* This returns the sum of all log file's estimated size in bytes. */
    return sum(values);
}
