const bodyPix = require('@tensorflow-models/body-pix');
const inkjet = require('inkjet');
const tfjs = require("@tensorflow/tfjs");
const fs = require('fs');
const { createCanvas, loadImage, createImageData, Image } = require('canvas');

const architecture = {
    architecture: 'MobileNetV1',
    outputStride: 16,
    multiplier: 0.5,
    quantBytes: 2
};

async function loadAndPredict(data,srcimagefile,net) {
  const segmentation = await net.segmentPersonParts(data);
  srcname = srcimagefile.substring(0,srcimagefile.indexOf("."));
  saveAsJson(segmentation,srcname+'_sgmt.json');
}

function saveAsJson(segImg,filename){
  var jsonStr = JSON.stringify(segImg);
  fs.writeFile(filename,jsonStr, function(err){
    if(err){
      console.log(err);
    }
  });
}

function convImg(data,srcimagefile){
  console.log(srcimagefile);
  imgD = createImageData(new Uint8ClampedArray(data.data), data.width, data.height);
  const img = new Image();
  img.src = srcimagefile;
  const canvas = createCanvas(data.width,data.height);
  const ctx = canvas.getContext('2d');
  ctx.drawImage(img,0,0,data.width,data.height);
  return tfjs.browser.fromPixels(canvas);
}

async function main() {
  var srcdir = process.argv[2];
  console.log(srcdir);
  
  const architecture = {
      architecture: 'MobileNetV1',
      outputStride: 16,
      multiplier: 0.5,
      quantBytes: 2
  };
  
  console.log("loading architeture");
  const net = await bodyPix.load(architecture);
  console.log(net)

  var srcimgs = fs.readdirSync(srcdir);

  srcimgs.forEach(function(item){
    if(!item.includes(".jpg")) 
      return;
    var combname = (srcdir+item);
    var readimg = fs.readFileSync(srcdir+item);
    inkjet.decode(readimg, function(err, data){
          if(err) throw err;
          var img = convImg(data,combname);
          loadAndPredict(img,combname,net).catch(e => {console.error(e)})
      });
  })
}
main();
