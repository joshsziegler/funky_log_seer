function(doc) {
    if(doc.Content) {
        /* This is an estimation based on UTF-16 */
        var est_size_in_bytes = (doc.Content.length * 2)
        emit(doc.key, est_size_in_bytes);
    }
}
