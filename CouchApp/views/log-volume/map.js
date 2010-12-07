function(doc) {
    if(doc.Content, doc.Year, doc.Month, doc.Day, doc.Hour) {
        /* This is an estimation based on UTF-16 */
        var est_size_in_bytes = (doc.Content.length * 2)
        /* TODO: Allow for a range of dates to compute est_size_in_bytes for
         * volume/time */
        emit(doc.key, est_size_in_bytes);
    }
}
