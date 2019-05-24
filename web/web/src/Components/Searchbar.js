import React from 'react';

const imageUrl = [
    'https://www.mirchi9.com/wp-content/uploads/2017/03/Same-Applause-for-Small-Movie-Nagaram-in-Tamil-and-Telugu-1.jpg',
    'https://i.axs.com/2018/01/49295-optimized_5a622145d1616.jpg',
    'https://i.ebayimg.com/images/g/VGoAAOSwnJtb-EnG/s-l300.jpg',
    'https://i0.wp.com/headsup.boyslife.org/files/2018/07/Alpha-photo_073018.jpg?ssl=1',
    'https://i0.wp.com/www.thelegendariumpodcast.com/wp-content/uploads/2018/07/small-banner-Rothfuss.jpg?fit=400%2C200',
    'https://i2.wp.com/pacificsun.com/wp-content/uploads/2018/09/smallfoot-banner.jpg?fit=600%2C350&ssl=1',
    'https://images-eds-ssl.xboxlive.com/image?url=8Oaj9Ryq1G1_p3lLnXlsaZgGzAie6Mnu24_PawYuDYIoH77pJ.X5Z.MqQPibUVTcJy_8qRqFcy_E.a.ZHo8ybhhOlYzafQmQ.aL4NND4_fQnebGXSkYzZ_P4e5hXNaKVoXmoz.Ia6yRygxXvWkPyMbKpCw9w9c.6dzw87dKrlYJgVfsTjAE9wGPfG1epv5wh8WOemzGnuUYiTljsxVT2WWKzTSltOS06cr9hu3lFqaA-&h=1080&w=1920&format=jpg',
    'https://cdn-media.threadless.com/challenges/Horror_Movie_Poster_smallbanner.jpg',
    'http://www.small-screen.co.uk/wp-content/uploads/2018/04/thumb-1920-709077-e1524154714285-1050x451.jpg',
    'https://cdn.empireonline.com/jpg/70/0/0/640/480/aspectfit/0/0/0/0/0/0/c/reviews_films/5820a64fff0f93a204914c7e/Hei%20Hei.jpg',
    'http://nyalicinemax.com/wp-content/uploads/2018/09/mile-22-banner-600x300.jpg',
    'https://www.mirchi9.com/wp-content/uploads/2017/03/Same-Applause-for-Small-Movie-Nagaram-in-Tamil-and-Telugu-1.jpg',
    'https://i.axs.com/2018/01/49295-optimized_5a622145d1616.jpg',
    'https://i.ebayimg.com/images/g/VGoAAOSwnJtb-EnG/s-l300.jpg',
    'https://i0.wp.com/headsup.boyslife.org/files/2018/07/Alpha-photo_073018.jpg?ssl=1',
    'https://i0.wp.com/www.thelegendariumpodcast.com/wp-content/uploads/2018/07/small-banner-Rothfuss.jpg?fit=400%2C200',
    'https://i2.wp.com/pacificsun.com/wp-content/uploads/2018/09/smallfoot-banner.jpg?fit=600%2C350&ssl=1',
    'https://images-eds-ssl.xboxlive.com/image?url=8Oaj9Ryq1G1_p3lLnXlsaZgGzAie6Mnu24_PawYuDYIoH77pJ.X5Z.MqQPibUVTcJy_8qRqFcy_E.a.ZHo8ybhhOlYzafQmQ.aL4NND4_fQnebGXSkYzZ_P4e5hXNaKVoXmoz.Ia6yRygxXvWkPyMbKpCw9w9c.6dzw87dKrlYJgVfsTjAE9wGPfG1epv5wh8WOemzGnuUYiTljsxVT2WWKzTSltOS06cr9hu3lFqaA-&h=1080&w=1920&format=jpg',
    'https://cdn-media.threadless.com/challenges/Horror_Movie_Poster_smallbanner.jpg',
    'http://www.small-screen.co.uk/wp-content/uploads/2018/04/thumb-1920-709077-e1524154714285-1050x451.jpg',
    'https://cdn.empireonline.com/jpg/70/0/0/640/480/aspectfit/0/0/0/0/0/0/c/reviews_films/5820a64fff0f93a204914c7e/Hei%20Hei.jpg',
    'http://nyalicinemax.com/wp-content/uploads/2018/09/mile-22-banner-600x300.jpg'
]

class Searchbar extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            raw_input: null,
            products: []
        };
    }

    handleChange(e) {
        let input = e.target.value
        this.setState({
            raw_input: input
        });
    }

    parseGenres(string) {
        string = string.replace('[', '');
        string = string.replace(']', '');
        string = string.split('\'').join('');
        string = string.split(' ').join('');
        let array = string.split(',');
        let s = array[0].charAt(0).toUpperCase() + array[0].slice(1);
        for (var k in array) {
            if (k == 0) { continue;}
            s = s + ", " + array[k].charAt(0).toUpperCase() + array[k].slice(1);
        }
        return(s)
    }

    parseOverview(string) {
        return(string.slice(0,45)+"...")
    }

    renderSingleProductPage(index, data){
        

		var page = $('.single-product'),
			container = $('.single-product .preview-large');
		// Find the wanted product by iterating the data object and searching for the chosen index.
		if(data.length){
			data.forEach(function (item) {
				if(item.id == index){
					// Populate '.preview-large' with the chosen product's data.
					container.find('h3').text(item.title);
					container.find('img').attr('src', item.image);
					container.find('p').text(item.overview_full);
				}
			});
		}

		// Show the page.
		page.addClass('visible');

        page.find('span').on('click', (e) => {
            e.preventDefault();
            window.location.hash = "";
            page.removeClass('visible');
        })
    }
    
    renderErrorPage() {
        window.location.hash = "itemNotFound";

        var page = $('.error');
        page.addClass('visible');

        page.find('span').on('click', (e) => {
            e.preventDefault();
            window.location.hash = "";
            page.removeClass('visible');
        })
    }

    rawData(url) {
        fetch(url)
        .then ((response) => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Error')
            }
        })
        .then ((data) => {
            let dataApi = data.data;
            let listData = [];

            for (var index in dataApi) {
                var obj = {};
                obj['id'] = index;
                obj['image'] = imageUrl[Math.floor(Math.random() * 22)];
                obj['title'] = dataApi[index][0];
                obj['vote_average'] = dataApi[index][1];
                obj['overview_short'] = this.parseOverview(dataApi[index][2]);
                obj['overview_full'] = dataApi[index][2];
                obj['genres'] = this.parseGenres(dataApi[index][3]);
                obj['score'] = dataApi[index][4];
                listData.push(obj);
            }

            this.setState({
                products : listData
            });

            var list = $('.all-products .products-list');

            // Remove previouse suggestions
            var size = list.children().size();
            if (size >= 1){
                $(".all-products .products-list li").remove();
            }

            var theTemplateScript = $("#products-template").html();
            var theTemplate = Handlebars.compile(theTemplateScript);
            list.append(theTemplate(this.state.products));
            
		    list.find('li').on('click', (e) => {
    			e.preventDefault();
                var productIndex = e.currentTarget.getAttribute("data-index");
                window.location.hash = 'product/' + productIndex;
                this.renderSingleProductPage(productIndex, this.state.products);
            })
        })
        .catch((error) => {
            this.renderErrorPage();
            console.log("Error Status: ", error);
        })
    }

    handleClick(event) {
        let hostGateway = "172.20.0.8"
        let input = document.getElementById("input").value
        this.setState({
            raw_input: input
        });

        console.log("inpput", input);

        var model = $('input[name=model]:checked', '#model').val();
        console.log("model ", model);
        
        let url ="";
        switch(model) {
            case "user":
                url = "http://" + hostGateway + ":8000/recommend/user/?title=" + input + "&k=8";
                break;
            case "content":
                url = "http://" + hostGateway + ":8000/recommend/content/?title=" + input + "&mode=content&k=8";
                break;
            case "keyword":
                url = "http://" + hostGateway + ":8000/recommend/content/?title=" + input + "&mode=keyword&k=8";
                break;
        }

        this.rawData(url);
    }

    componentDidMount() {
        var options = {
            url: "src/Components/title.json",

            getValue: "name",

            list: {
                maxNumberOfElements: 8,
                match: {
                    enabled: true
                },
                onChooseEvent: () => {
                    var value = $("#searchbar #input").getSelectedItemData();
                    console.log(value);
                    this.handleClick(value);
                    // $("#data-holder").val(value).trigger("change");
                }
            },

            theme: "plate-dark"
        };
        
        $("#searchbar #input").easyAutocomplete(options)
    }

    

    // generateAllProductsHTML(){

    //     fetch('/src/Components/products.json')
    //     .then ((response) => {
    //         console.log("response ", response)
    //         return response.json();
    //     })
    //     .then ((data) => {
    //         console.log("data ", data)
    //         this.setState({
    //             products : data
    //         });

    //         var list = $('.all-products .products-list');
    //         var theTemplateScript = $("#products-template").html();
    //         var theTemplate = Handlebars.compile(theTemplateScript);
    //         list.append(theTemplate(this.state.products));

	// 	    list.find('li').on('click', function (e) {
    // 			e.preventDefault();
	// 		    var productIndex = $(this).data('index');
	// 		    window.location.hash = 'product/' + productIndex;
    //         })
    //     })
    //     .catch((error) => {
    //         console.log("Error Status: ", error)
    //     })

		
	// }


    render () {
        return (
            <div>
                <input 
                    type="text"
                    id="input"
                    className="input"
                    placeholder ="Toy Story, Batman Returns...">
                </input>
                <button
                    onClick={e => this.handleClick(e)}> 
                    Submit
                </button>
            </div>
        )
    }
}

export default Searchbar;