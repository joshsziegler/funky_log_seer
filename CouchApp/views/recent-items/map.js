function(doc) {
  if (doc.Content && doc.Host && doc.File) {
    emit(null, doc);
    emit(doc.Host, doc);
    emit(doc.Host+doc.File, doc);
  }
};
