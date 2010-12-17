function(doc) {
    if(doc.Host) {
        emit(null, doc.Host);
    }
}
