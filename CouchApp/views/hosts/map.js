function(doc) {
    if(doc.Content && doc.Host) {
        emit(doc.Host, null);
    }
}
