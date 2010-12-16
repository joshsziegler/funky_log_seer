function(doc) {
    if(doc.Content, doc.Year, doc.Month, doc.Day, doc.Hour) {
        /* This is an estimation based on UTF-16 encoding */
        var est_size_in_bytes = (doc.Content.length * 2);
        date_key = String(doc.Year) + String(doc.Month) + String(doc.Day);
        emit({date: date_key}, est_size_in_bytes);
        emit({date:date_key, hour:doc.Hour}, est_size_in_bytes);
    }
}
