import React, { Component } from 'react';
import D3KG from './components/D3KG'
import { Icon, Label, Menu, Table } from 'semantic-ui-react'
// import { CsvToHtmlTable } from 'react-csv-to-table';
// import sampleData from './assets/paper_info/nilm_100_exact_author_expertise.csv'
// import jsonData from './assets/paper_info/nilm_100_exact_author_knowledge';
import jsonData from './assets/ScholarTable.json';

const sampleData = `
Rank,Author,Title,Citations,Year,Source,Abstract
46, Shulman,Basic knowledge and the problem of easy knowledge,28089,1986,https://www.pdcnet.org/ppr/content/ppr_2002_0065_0002_0309_0329,""" He who can, does. He who cannot, teaches.“1 don't know in what fit of pique George Bernard Shaw wrote that infamous aphorism, words that have plagued members of the teaching profession for nearly a century. They are found in"" Maxims for Revolutionists,"" an "
7, Hayek,The use of knowledge in society,18749,1945,https://www.jstor.org/stable/1809376,"On certain familiar assumptions the answer is simple enough. If we possess all the relevant information, if we can start out from a given system of preferences and if we command complete knowledge of available means, the problem which remains is purely one of logic "
64,Habermas,The concept of knowledge and how to measure it,15305,2015,https://www.emerald.com/insight/content/doi/10.1108/14691930310455414/full/html,Habermas describes Knowledge and Human Interests as an attempt to reconstruct the prehistory of modern positivism with the intention of analysing the connections between knowledge and human interests. Convinced of the increasing historical and social 
80, Popper,Sustainable knowledge,13059,1972,https://www.sciencedirect.com/science/article/pii/0016718594900108,"MAN, some modern philosophers tell us, is alienated from his world: he is a stranger and afraid in a world he never made. Perhaps he is; yet so are animals, and even plants. They too were born, long ago, into a physicochemical world, a world they never made. But "
54,Minsky,Origins of knowledge.,12477,1974,https://psycnet.apa.org/record/1993-05134-001,"Here is the essence of the frame theory: When one encounters a new situation (or makes a substantial change in one's view of a problem), one selects from memory a structure called a frame. This is a remembered framework to be adapted to fit reality by changing details as "

`;


class App extends Component {
  
  constructor(props) {
    super(props);
  }

  render() {
    // console.log(Object.entries(jsonData));
    return (
      <div>
        <D3KG/>

      </div>
    );
  }
}

export default App;
