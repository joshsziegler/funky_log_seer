function(doc) {
  if (doc.Content && doc.Host && doc.File) {
    emit("all", doc);
    emit(doc.Host, doc);
    emit(doc.Host+doc.File, doc);
  }
};
