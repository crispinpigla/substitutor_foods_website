

//           Envoie de la demande de substitution 



$('.un_suscribe').click(function(){

	var id_product = this.getAttribute('id_product');
	var id_substitut = this.getAttribute('id_substitut');
     
    $.ajax({
       url : 'substitute/?un_suscribe_substitute_id=' + id_substitut + '&id_product=' + id_product,
       type : 'GET',
       dataType : 'html',
       success : function(code_html, statut){

        console.log(code_html == 'not_connected');

        if ( code_html == 'not_connected' ) 
        {
        	window.location.href = "/substitutor/home/?home_status=connexion";
        }
        else
        {
        	$('#un_suscribe_'+id_substitut + '_' + id_product).parent().html(code_html)
        }
           
       },

       error : function(resultat, statut, erreur){

       	console.log('le resultat de l\'erreur : ', resultat);
       	console.log(' l\'erreur : ', erreur);
       	console.log('le statut : ', statut);

       },

       complete : function(resultat, statut){

       }

    });




});














$('.un_suscribe_favorites').click(function(){

	var id_product = this.getAttribute('id_product');
	var id_substitut = this.getAttribute('id_substitut');
     
    $.ajax({
       url : 'substitute/?un_suscribe_substitute_id=' + id_substitut + '&id_product=' + id_product,
       type : 'GET',
       dataType : 'html',
       success : function(code_html, statut){


        console.log(code_html);
        $('#un_suscribe_'+id_substitut + '_' + id_product).parent().parent().parent().remove();
           
       },

       error : function(resultat, statut, erreur){

       },

       complete : function(resultat, statut){

       }

    });


});



$('.conteneur_produit').mouseover(function() {$(this).css('background', 'rgb(230,230,230)')});
$('.conteneur_produit').mouseout(function() {$(this).css('background', 'rgb(245, 245, 245)')});


$('.un_suscribe').mouseover(function() {
	if ( ($(this).text()).indexOf('Enregistrer ce produit') != -1 ) 
	{
		$(this).css('background', 'white');
		$(this).css('color', 'green' );
	}
	else
	{
		$(this).css('background', 'white');
		$(this).css('color', 'red' );
	}
});


$('.un_suscribe').mouseout(function() {
	var background = $(this).css('color');
	$(this).css('background', background)
	$(this).css('color', 'white')
});


$('.un_suscribe_favorites').mouseover(function() {
	if ( ($(this).text()).indexOf('Enregistrer ce produit') != -1 ) 
	{
		$(this).css('background', 'white');
		$(this).css('color', 'green' );
	}
	else
	{
		$(this).css('background', 'white');
		$(this).css('color', 'red' );
	}
});


$('.un_suscribe_favorites').mouseout(function() {
	var background = $(this).css('color');
	$(this).css('background', background)
	$(this).css('color', 'white')
});




$('.un_suscribe').attr('class', 'un_suscribe_off');



//        Envoie de commentaire


$('.send_comment_button').click(function(){

  var id_product = this.getAttribute('id_product');
  var comment_text = $(this).siblings('textarea').val();
     
    $.ajax({
       url : '../comments/?id_product_comments=' + id_product + '&comment_text=' + comment_text,
       type : 'GET',
       dataType : 'html',
       success : function(code_html, statut){

        console.log(code_html == 'not_connected');

        if ( code_html == 'not_connected' ) 
        {
          window.location.href = "/substitutor/home/?home_status=connexion";
        }
        else
        {
          $('.message_confirmation_publication').css('display','block');
          $('textarea').val('');
          setTimeout(function(){ $('.message_confirmation_publication').css('display','none'); }, 5000);
        }
           
       },

       error : function(resultat, statut, erreur){

         console.log('le resultat de l\'erreur : ', resultat);
         console.log(' l\'erreur : ', erreur);
         console.log('le statut : ', statut);

       },

       complete : function(resultat, statut){

       }

    });




});
