//Entrar com o tile landsat como Table (importar como assest e inserir)

Map.addLayer(table);

//Filtro nuvem

function MascaraNubesS(image) {
  var qa = image.select('QA60');
  var RecorteNubesMascaraS = 1 << 10;
  var RecorteCirrosMascaraS = 1 << 11;
  var MascaraS = qa.bitwiseAnd(RecorteNubesMascaraS).eq(0)
      .and(qa.bitwiseAnd(RecorteCirrosMascaraS).eq(0));
  return image.updateMask(MascaraS);}

// Selecao da colecao

var collection = ee.ImageCollection('COPERNICUS/S2_SR') // Sentinel 2 SR...
  .filterDate('2020-07-01', '2020-08-01') //Filtrar por data
  .filterBounds(table) //No shape passado
  .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 10)) // filtro de catalogo com 10% de nuvem
  .map(MascaraNubesS); //aplica a mascara de nuvens
  
  
print(collection); // gera a lista de imagens obtidas
  
// reduzindo as imagens pra mediana

var medianpixels = collection.median(); // seleciona a mediana para a composicao
var medianpixelsclipped = medianpixels.clip(table); // recorta pela area   

// visualiza o mosaico - pode escolher as bandas que quiser e o contraste
Map.addLayer(medianpixelsclipped, {bands: ['B8', 'B4', 'B3'], min: 0, max: 10000, gamma: 1.5}, 'Sentinel_2 mosaic');

//selecionando bandas pra exportar
var medianexport = medianpixelsclipped.select(['B2','B3', 'B4', 'B8']);


//-- Exportação
Export.image.toDrive({
  image:medianexport,
  description: '217_71_217_72', //nome do arquivo
  folder: 'Engine', //pasta
  maxPixels:1e9,
  scale: 10,
  fileFormat: 'GeoTIFF',
  crs: 'EPSG:4326',
  region: table
});