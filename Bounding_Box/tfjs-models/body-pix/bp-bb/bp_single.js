const bodyPix = require('@tensorflow-models/body-pix');
const inkjet = require('inkjet');
const tfjs = require("@tensorflow/tfjs");
const fs = require('fs');
const { createCanvas, loadImage, createImageData, Image } = require('canvas');

var srcimagefile = process.argv[2]

const architecture = {
    architecture: 'MobileNetV1',
    outputStride: 16,
    multiplier: 0.5,
    quantBytes: 2
};

async function loadAndPredict(data) {
  console.log(data)
  console.log("loading architecture");
  const net = await bodyPix.load(architecture);
  console.log()
  console.log("segmenting person");
  const segmentation = await net.segmentPersonParts(data);
  //console.log(segmentation);
  srcname = srcimagefile.substring(0,srcimagefile.indexOf("."));
  saveAsJson(segmentation,srcname+'_sgmt.json');
  //writeToFile(segmentation.data,segmentation.height,segmentation.width,'segmentation.txt');
  //saveImage(maskImage);
}

function saveAsJson(segImg,filename){
  var jsonStr = JSON.stringify(segImg);
  fs.writeFile(filename,jsonStr, function(err){
    if(err){
      console.log(err);
    }
  });
}

var srcimg = fs.readFileSync(srcimagefile);
console.log(srcimg)

function convImg(data){
  imgD = createImageData(new Uint8ClampedArray(data.data), data.width, data.height);
  const img = new Image();
  img.src = srcimagefile;
  const canvas = createCanvas(data.width,data.height);
  const ctx = canvas.getContext('2d');
  ctx.drawImage(img,0,0,data.width,data.height);
  return tfjs.browser.fromPixels(canvas);
}

inkjet.decode(srcimg, function(err, data){
    if(err) throw err;
    console.log("Image loaded.");
    var img = convImg(data);
    //console.log(img);
    loadAndPredict(img).catch(e => {console.error(e)})
});