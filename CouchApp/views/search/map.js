function(doc) {
    if(doc.Content && doc.File && doc.Host) {
        if(doc.Content.search(/error/i) != -1){
            emit(doc.key, doc);
        }
    }
}
