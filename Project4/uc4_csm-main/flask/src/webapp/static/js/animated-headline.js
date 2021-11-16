jQuery(document).ready(function($){

	// set animation timing
	const animationDelay = 1000,
		// letters effect
		lettersDelay = 100,
		// time interval param
		timeInterval = 1000,
		showCnt = 1; // timeInterval * showCnt (ms)

	let count = 0;
	let httpRequest;
	let resTxt = $('.res-text');

	// start the function
	initHeadline();

	function initHeadline() {
		//insert <i> element for each letter of a changing word
		singleLetters($('.box-headline.letters').find('b'));
		//initialise headline animation
		//animateHeadline($('.box-headline'));
		intervalReq = setInterval(makeRequest,timeInterval);
	}

	function singleLetters($words) {
		$words.each(function(){
			let word = $(this),
				letters = word.text().split(''),
				selected = word.hasClass('is-visible');
			for (i in letters) {
				if(selected){
					if(word.parents('.rotate-2').length > 0) letters[i] = '<em>' + letters[i] + '</em>';
					letters[i] = '<i class="in">' + letters[i] + '</i>';
				}
				else{
					if(word.parents('.rotate-2').length > 0) letters[i] = (letters[i]=='A')?'<em><font color="red">' + letters[i] + '</font></em>'
																			:(letters[i]=='B')?'<em><font color="blue">' + letters[i] + '</font></em>'
																			:'<em>' + letters[i] + '</em>';
					letters[i] = '<i>' + letters[i] + '</i>';
				}
				
			}

			let newLetters = letters.join('');
			word.html(newLetters).css('opacity', 1);
		});
	}

	function makeRequest() {
		if(count>0){

			if(count===showCnt){
				count = -1;
			}
			else{
				count = count + 1;
			}
		}
		else{
			httpRequest = new XMLHttpRequest();
			httpRequest.onreadystatechange = alertContents;
			if(!httpRequest) {
				alert("Can't make XMLHTTP Instance");
				return false;
			}

			httpRequest.open('GET', 'calculate');
			httpRequest.send();
		}
	}

	function alertContents() {
		let headline = $('.box-headline');
		let result;
		let word,nextWord;
		let newRes;
		try {
			if (httpRequest.readyState === XMLHttpRequest.DONE) {

				if (httpRequest.status === 200) {
					result = httpRequest.responseText;
					word = headline.find('.is-visible').eq(0);

					// if the crrunt word is not same with the next word
					if(!word.hasClass(result)){

						if(count===-1 || result==='NA'){
							// previously, It was an 'A' or 'B'
							// In this part, must show a main page regardless of a current result
							nextWord = headline.find('.NA').eq(0);
							resTxt.text("Ambient intelligence for office environments");
							count = 0;
						}
						else{
							newRes = '.'.concat(result);
							nextWord = headline.find(newRes).eq(0);

							if(result==='A'){
								resTxt.text("YOU NEED TO GO TO ROOM NO.5");
								if(count === 0){
									count = 1;
								}
							}
							else if(result==='B'){
								resTxt.text("YOU NEED TO GO TO ROOM NO.6");
								if(count === 0){
									count = 1;
								}
							}
						}
						// change the intro word
						console.log(result);
						hideWord(word,nextWord);

					}

				}
				else {
					let word = headline.find('.is-visible').eq(0);
					if(!word.hasClass('NA')){
						//if not 'NA', chane to the 'NA'
						let nextWord = headline.find(".NA").eq(0);
						hideWord(word,nextWord);
					}

					//hideWord( headline.find('.is-visible').eq(0) );
					//alert("There was a problem with the request.");
				}
			}
		}
		catch(e){
			alert('Caught Exception: ' + e.description);
		}
	}

	function hideWord($word,$nextWord) {

		if($word.parents('.box-headline').hasClass('letters')) {
			let bool = ($word.children('i').length >= $nextWord.children('i').length) ;
			hideLetter($word.find('i').eq(0), $word, bool, lettersDelay);
			showLetter($nextWord.find('i').eq(0), $nextWord, bool, lettersDelay);
			$word.removeClass('is-visible');
			$nextWord.addClass('is-visible');

		}
	}

	function hideLetter($letter, $word, $bool, $duration) {
		$letter.removeClass('in').addClass('out');

		if(!$letter.is(':last-child')) {
			setTimeout(function(){ hideLetter($letter.next(), $word, $bool, $duration); }, $duration);
		}

	}

	function showLetter($letter, $word, $bool, $duration) {
		$letter.addClass('in').removeClass('out');

		if(!$letter.is(':last-child')) {
			setTimeout(function(){ showLetter($letter.next(), $word, $bool, $duration); }, $duration);
		} else {
			if($word.parents('.box-headline').hasClass('type')) { setTimeout(function(){ $word.parents('.box-words-wrapper').addClass('waiting'); }, 200);}
			//if(!$bool) { setTimeout(function(){ hideWord($word) }, animationDelay) }
		}
	}


	function closePage(){

		clearInterval(intervalReq);

	}

});