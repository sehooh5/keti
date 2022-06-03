const mongoose = require('mongoose');

const { Schema } = mongoose;
const { Types: { ObjectID } } = Schema;
const commentSchema = new Schema({
    commenter:{
        type: ObjectId,
        required: true,
        ref: 'User',
    },
    comment:{
        type: String,
        required: true,
    },
    commentAt: {
        type: Date,
        default: Date.now,
    },
});

module.export = mongoose.model('Comment', commentSchema);