const mongoose = require('mongoose');

const { Schema } = mongoose;
const userSchema = new Schema({
    name:{
        type: String,
        required: true,
        unique: true,
    },
    age:{
        type: String,
        required: true,
    },
    married:{
        type: Boolean,
        required: true,
    },
    comment: String,
    createdAt: {
        type: Date,
        default: Date.now,
    },
});

module.export = mongoose.model('User', userSchema);