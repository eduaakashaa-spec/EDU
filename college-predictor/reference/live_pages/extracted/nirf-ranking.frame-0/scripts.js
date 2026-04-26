

const DATA = [{"id":"IR-E-U-0456","name":"Indian Institute of Technology Madras","city":"Chennai","state":"Tamil Nadu","score":88.72,"rank":1,"band":"Rank 1 -100","url":"https://www.iitm.ac.in","type":"IIT"},{"id":"IR-E-I-1074","name":"Indian Institute of Technology Delhi","city":"New Delhi","state":"Delhi","score":85.74,"rank":2,"band":"Rank 1 -100","url":"https://home.iitd.ac.in","type":"IIT"},{"id":"IR-E-U-0306","name":"Indian Institute of Technology Bombay","city":"Mumbai","state":"Maharashtra","score":83.65,"rank":3,"band":"Rank 1 -100","url":"https://www.iitb.ac.in","type":"IIT"},{"id":"IR-E-I-1075","name":"Indian Institute of Technology Kanpur","city":"Kanpur","state":"Uttar Pradesh","score":81.82,"rank":4,"band":"Rank 1 -100","url":"https://www.iitk.ac.in","type":"IIT"},{"id":"IR-E-U-0573","name":"Indian Institute of Technology Kharagpur","city":"Kharagpur","state":"West Bengal","score":78.69,"rank":5,"band":"Rank 1 -100","url":"https://www.iitkgp.ac.in","type":"IIT"},{"id":"IR-E-U-0560","name":"Indian Institute of Technology Roorkee","city":"Roorkee","state":"Uttarakhand","score":75.44,"rank":6,"band":"Rank 1 -100","url":"https://www.iitr.ac.in","type":"IIT"},{"id":"IR-E-U-0013","name":"Indian Institute of Technology Hyderabad","city":"Hyderabad","state":"Telangana","score":72.31,"rank":7,"band":"Rank 1 -100","url":"https://www.iith.ac.in","type":"IIT"},{"id":"IR-E-U-0053","name":"Indian Institute of Technology Guwahati","city":"Guwahati","state":"Assam","score":72.24,"rank":8,"band":"Rank 1 -100","url":"https://www.iitg.ac.in","type":"IIT"},{"id":"IR-E-U-0467","name":"National Institute of Technology Tiruchirappalli","city":"Tiruchirappalli","state":"Tamil Nadu","score":68.14,"rank":9,"band":"Rank 1 -100","url":"https://www.nitt.edu","type":"NIT"},{"id":"IR-E-U-0701","name":"Indian Institute of Technology (Banaras Hindu University) Varanasi","city":"Varanasi","state":"Uttar Pradesh","score":67.24,"rank":10,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"IIT"},{"id":"IR-E-U-0391","name":"Birla Institute of Technology & Science -Pilani","city":"Pilani","state":"Rajasthan","score":67.02,"rank":11,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"BITS"},{"id":"IR-E-U-0273","name":"Indian Institute of Technology Indore","city":"Indore","state":"Madhya Pradesh","score":66.65,"rank":12,"band":"Rank 1 -100","url":"https://www.iiti.ac.in","type":"IIT"},{"id":"IR-E-U-0357","name":"National Institute of Technology Rourkela","city":"Rourkela","state":"Odisha","score":66.62,"rank":13,"band":"Rank 1 -100","url":"https://www.nitr.ac.in","type":"NIT"},{"id":"IR-E-U-0473","name":"S.R.M. Institute of Science and Technology","city":"Chennai","state":"Tamil Nadu","score":65.83,"rank":14,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0205","name":"Indian Institute of Technology (Indian School of Mines)","city":"Dhanbad","state":"Jharkhand","score":65.37,"rank":15,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"IIT"},{"id":"IR-E-U-0490","name":"Vellore Institute of Technology","city":"Vellore","state":"Tamil Nadu","score":65.25,"rank":16,"band":"Rank 1 -100","url":"https://vit.ac.in","type":"Private"},{"id":"IR-E-U-0237","name":"National Institute of Technology Karnataka, Surathkal","city":"Surathkal","state":"Karnataka","score":64.59,"rank":17,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"NIT"},{"id":"IR-E-U-0575","name":"Jadavpur University","city":"Kolkata","state":"West Bengal","score":64.54,"rank":18,"band":"Rank 1 -100","url":"https://jadavpuruniversity.in","type":"University"},{"id":"IR-E-U-0064","name":"Indian Institute of Technology Patna","city":"Patna","state":"Bihar","score":64.52,"rank":19,"band":"Rank 1 -100","url":"https://www.iitp.ac.in","type":"IIT"},{"id":"IR-E-U-0439","name":"Anna University","city":"Chennai","state":"Tamil Nadu","score":63.51,"rank":20,"band":"Rank 1 -100","url":"https://www.annauniv.edu","type":"University"},{"id":"IR-E-U-0263","name":"National Institute of Technology Calicut","city":"Kozhikode","state":"Kerala","score":63.05,"rank":21,"band":"Rank 1 -100","url":"https://www.nitc.ac.in","type":"NIT"},{"id":"IR-E-U-0363","name":"Siksha `O` Anusandhan","city":"Bhubaneswar","state":"Odisha","score":62.58,"rank":22,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0436","name":"Amrita Vishwa Vidyapeetham","city":"Coimbatore","state":"Tamil Nadu","score":62.46,"rank":23,"band":"Rank 1 -100","url":"https://www.amrita.edu","type":"University"},{"id":"IR-E-U-0108","name":"Jamia Millia Islamia","city":"New Delhi","state":"Delhi","score":62.42,"rank":24,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0139","name":"Indian Institute of Technology Gandhinagar","city":"Gandhinagar","state":"Gujarat","score":62.31,"rank":25,"band":"Rank 1 -100","url":"https://www.iitgn.ac.in","type":"IIT"},{"id":"IR-E-U-0184","name":"Indian Institute of Technology Mandi","city":"Mandi","state":"Himachal Pradesh","score":62.08,"rank":26,"band":"Rank 1 -100","url":"https://www.iitmandi.ac.in","type":"IIT"},{"id":"IR-E-U-0395","name":"Indian Institute of Technology Jodhpur","city":"Jodhpur","state":"Rajasthan","score":61.31,"rank":27,"band":"Rank 1 -100","url":"https://www.iitj.ac.in","type":"IIT"},{"id":"IR-E-U-0025","name":"National Institute of Technology Warangal","city":"Warangal","state":"Telangana","score":61.05,"rank":28,"band":"Rank 1 -100","url":"https://www.nitw.ac.in","type":"NIT"},{"id":"IR-E-I-1480","name":"Thapar Institute of Engineering and Technology (Deemed-to-be-university)","city":"Patiala","state":"Punjab","score":60.97,"rank":29,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"University"},{"id":"IR-E-U-0098","name":"Delhi Technological University","city":"New Delhi","state":"Delhi","score":60.85,"rank":30,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0747","name":"Chandigarh University","city":"Mohali","state":"Punjab","score":60.46,"rank":31,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0378","name":"Indian Institute of Technology Ropar","city":"Rupnagar","state":"Punjab","score":59.66,"rank":32,"band":"Rank 1 -100","url":"https://www.iitrpr.ac.in","type":"IIT"},{"id":"IR-E-U-0458","name":"Kalasalingam Academy of Research and Education","city":"Krishnan Koil","state":"Tamil Nadu","score":59.03,"rank":33,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0496","name":"Aligarh Muslim University","city":"Aligarh","state":"Uttar Pradesh","score":59.01,"rank":34,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0020","name":"Koneru Lakshmaiah Education Foundation University (K L College of Engineering)","city":"Vaddeswaram","state":"Andhra Pradesh","score":58.95,"rank":35,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0356","name":"Kalinga Institute of Industrial Technology","city":"Bhubaneswar","state":"Odisha","score":58.79,"rank":36,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0497","name":"Amity University","city":"Gautam Budh Nagar","state":"Uttar Pradesh","score":58.53,"rank":37,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0014","name":"International Institute of Information Technology Hyderabad","city":"Hyderabad","state":"Telangana","score":58.45,"rank":38,"band":"Rank 1 -100","url":"https://www.iiit.ac.in","type":"Private"},{"id":"IR-E-U-0355","name":"Indian Institute of Technology Bhubaneswar","city":"Bhubaneswar","state":"Odisha","score":58.22,"rank":39,"band":"Rank 1 -100","url":"https://www.iitbbs.ac.in","type":"IIT"},{"id":"IR-E-U-0476","name":"Shanmugha Arts Science Technology & Research Academy","city":"Thanjavur","state":"Tamil Nadu","score":58.02,"rank":40,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0308","name":"Institute of Chemical Technology","city":"Mumbai","state":"Maharashtra","score":57.96,"rank":41,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0410","name":"Malaviya National Institute of Technology","city":"Jaipur","state":"Rajasthan","score":57.45,"rank":42,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"NIT"},{"id":"IR-E-U-0564","name":"UPES","city":"Dehradun","state":"Uttarakhand","score":56.99,"rank":43,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0334","name":"Visvesvaraya National Institute of Technology, Nagpur","city":"Nagpur","state":"Maharashtra","score":56.58,"rank":44,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"NIT"},{"id":"IR-E-I-1441","name":"Saveetha Institute of Medical and Technical Sciences","city":"Chennai","state":"Tamil Nadu","score":56.55,"rank":45,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"University"},{"id":"IR-E-U-0329","name":"Symbiosis International","city":"Pune","state":"Maharashtra","score":56.22,"rank":46,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-C-16604","name":"Sri Sivasubramaniya Nadar College of Engineering","city":"Kalavakkam","state":"Tamil Nadu","score":56.08,"rank":47,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0379","name":"Lovely Professional University","city":"Phagwara","state":"Punjab","score":55.99,"rank":48,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0577","name":"National Institute of Technology Durgapur","city":"Durgapur","state":"West Bengal","score":55.94,"rank":49,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"NIT"},{"id":"IR-E-U-0055","name":"National Institute of Technology Silchar","city":"Silchar","state":"Assam","score":55.91,"rank":50,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"NIT"},{"id":"IR-E-U-0202","name":"Birla Institute of Technology","city":"Ranchi","state":"Jharkhand","score":55.28,"rank":51,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"BITS"},{"id":"IR-E-U-0555","name":"Graphic Era University","city":"Dehradun","state":"Uttarakhand","score":55.26,"rank":52,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0072","name":"National Institute of Technology Patna","city":"Patna","state":"Bihar","score":53.89,"rank":53,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"NIT"},{"id":"IR-E-U-0584","name":"Indian Institute of Engineering Science and Technology, Shibpur","city":"Howrah","state":"West Bengal","score":53.63,"rank":54,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0374","name":"Dr. B R Ambedkar National Institute of Technology, Jalandhar","city":"Jalandhar","state":"Punjab","score":53.38,"rank":55,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"NIT"},{"id":"IR-E-U-0906","name":"Indian Institute of Technology Jammu","city":"Jammu","state":"Jammu and Kashmir","score":53.08,"rank":56,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"IIT"},{"id":"IR-E-U-0844","name":"Indian Institute of Technology, Tirupati","city":"Tirupati","state":"Andhra Pradesh","score":52.73,"rank":57,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"IIT"},{"id":"IR-E-U-0749","name":"Manipal University Jaipur","city":"Jaipur","state":"Rajasthan","score":52.69,"rank":58,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"University"},{"id":"IR-E-C-7252","name":"Manipal Institute of Technology","city":"Manipal","state":"Karnataka","score":52.55,"rank":59,"band":"Rank 1 -100","url":"https://manipal.edu/mit.html","type":"University"},{"id":"IR-E-U-0739","name":"Madan Mohan Malaviya University of Technology","city":"Gorakhpur","state":"Uttar Pradesh","score":52.45,"rank":60,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0255","name":"Indian Institute of Space Science and Technology","city":"Thiruvananthapuram","state":"Kerala","score":52.44,"rank":61,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0530","name":"Motilal Nehru National Institute of Technology","city":"Prayagraj","state":"Uttar Pradesh","score":52.15,"rank":62,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"NIT"},{"id":"IR-E-U-0105","name":"Indraprastha Institute of Information Technology","city":"New Delhi","state":"Delhi","score":51.33,"rank":63,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0878","name":"Indian Institute of Technology Palakkad","city":"Palakkad","state":"Kerala","score":51.2,"rank":64,"band":"Rank 1 -100","url":"https://iitpkd.ac.in","type":"IIT"},{"id":"IR-E-U-0622","name":"National Institute of Technology Delhi","city":"Delhi","state":"Delhi","score":50.79,"rank":65,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"NIT"},{"id":"IR-E-U-0149","name":"Sardar Vallabhbhai National Institute of Technology","city":"SURAT","state":"Gujarat","score":50.77,"rank":66,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"NIT"},{"id":"IR-E-U-0474","name":"Sathyabama Institute of Science and Technology","city":"Chennai","state":"Tamil Nadu","score":50.64,"rank":67,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-C-37013","name":"PSG College of Technology","city":"Coimbatore","state":"Tamil Nadu","score":50.64,"rank":67,"band":"Rank 1 -100","url":"https://www.psgtech.edu","type":"University"},{"id":"IR-E-U-0221","name":"International Institute of Information Technology Bangalore","city":"Bengaluru","state":"Karnataka","score":50.46,"rank":69,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-C-6379","name":"Netaji Subhas University of Technology (NSUT)","city":"Delhi","state":"Delhi","score":50.43,"rank":70,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0389","name":"Banasthali Vidyapith","city":"Banasthali","state":"Rajasthan","score":50.38,"rank":71,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0946","name":"Indian Institute of Technology Bhilai","city":"Durg","state":"Chhattisgarh","score":50.37,"rank":72,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"IIT"},{"id":"IR-E-U-0197","name":"National Institute of Technology Srinagar","city":"Srinagar","state":"Jammu and Kashmir","score":50.23,"rank":73,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"NIT"},{"id":"IR-E-U-0042","name":"University of Hyderabad","city":"Hyderabad","state":"Telangana","score":49.36,"rank":74,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-C-1331","name":"M. S. Ramaiah Institute of Technology","city":"Bengaluru","state":"Karnataka","score":49.26,"rank":75,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0217","name":"Christ University","city":"Bengaluru","state":"Karnataka","score":49.03,"rank":76,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0899","name":"Indian Institute of Technology Dharwad","city":"Dharwad","state":"Karnataka","score":48.61,"rank":77,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"IIT"},{"id":"IR-E-U-0535","name":"Rajiv Gandhi Institute of Petroleum Technology","city":"Amethi","state":"Uttar Pradesh","score":48.52,"rank":78,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0384","name":"Sant Longowal Institute of Engineering & Technology","city":"Longowal","state":"Punjab","score":48.42,"rank":79,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0043","name":"Vignan's Foundation for Science, Technology and Research","city":"Guntur","state":"Andhra Pradesh","score":48.27,"rank":80,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0284","name":"Maulana Azad National Institute of Technology","city":"Bhopal","state":"Madhya Pradesh","score":48.26,"rank":81,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"NIT"},{"id":"IR-E-U-0207","name":"National Institute of Technology, Jamshedpur","city":"Jamshedpur","state":"Jharkhand","score":48.25,"rank":82,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"NIT"},{"id":"IR-E-U-0619","name":"National Institute of Technology Meghalaya","city":"Shillong","state":"Meghalaya","score":48.21,"rank":83,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"NIT"},{"id":"IR-E-U-0223","name":"Jain university,Bangalore","city":"Bengaluru","state":"Karnataka","score":48.01,"rank":84,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0172","name":"National Institute of Technology Kurukshetra","city":"Kurukshetra","state":"Haryana","score":47.98,"rank":85,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"NIT"},{"id":"IR-E-U-0092","name":"National Institute of Technology, Raipur","city":"Raipur","state":"Chhattisgarh","score":47.59,"rank":86,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"NIT"},{"id":"IR-E-U-0489","name":"Vel Tech Rangarajan Dr. Sagunthala R & D Institute of Science and Technology","city":"Chennai","state":"Tamil Nadu","score":47.43,"rank":87,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-C-24004","name":"AU College of Engineering (A)","city":"Visakhapatnam","state":"Andhra Pradesh","score":47.37,"rank":88,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0373","name":"Chitkara University","city":"Rajpura","state":"Punjab","score":47.34,"rank":89,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-1257","name":"COEP Technological University","city":"Pune","state":"Maharashtra","score":47.31,"rank":90,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-C-19754","name":"SR University","city":"Warangal","state":"Telangana","score":47.16,"rank":91,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0297","name":"Defence Institute of Advanced Technology","city":"Pune","state":"Maharashtra","score":46.98,"rank":92,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0078","name":"Panjab University","city":"Chandigarh","state":"Chandigarh","score":46.9,"rank":93,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0017","name":"Jawaharlal Nehru Technological University","city":"Hyderabad","state":"Telangana","score":46.74,"rank":94,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-C-30045","name":"C.V. Raman Global University, Odisha","city":"Bhubaneswar","state":"Odisha","score":46.62,"rank":95,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0267","name":"Atal Bihari Vajpayee Indian Institute of Information Technology and Management","city":"Gwalior","state":"Madhya Pradesh","score":46.25,"rank":96,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"IIIT"},{"id":"IR-E-U-0189","name":"National Institute of Technology Hamirpur","city":"Hamirpur","state":"Himachal Pradesh","score":46.1,"rank":97,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"NIT"},{"id":"IR-E-U-0147","name":"Pandit Deendayal Energy University","city":"Gandhinagar","state":"Gujarat","score":45.97,"rank":98,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"IR-E-U-0621","name":"National Institute of Technology Puducherry","city":"Karaikal","state":"Pondicherry","score":45.83,"rank":99,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"NIT"},{"id":"IR-E-C-36995","name":"Sri Krishna College of Engineering and Technology","city":"Coimbatore","state":"Tamil Nadu","score":45.55,"rank":100,"band":"Rank 1 -100","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Amity University","city":"North Twenty Four Parganas","state":"West Bengal","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Amity University Haryana, Gurgaon","city":"Gurugram, Haryana","state":"Haryana","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Anurag University","city":"Hyderabad","state":"Telangana","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Bansilal Ramnath Agarwal Charitable Trust`s Vishwakarama Institute of Technology","city":"Pune","state":"Maharashtra","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Chandigarh Engineering College-CGC, Landran, Mohali","city":"Mohali","state":"Punjab","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Chennai Institute of Technology","city":"Chennai","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Coimbatore Institute of Technology","city":"Coimbatore","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"College of Engineering Trivandrum","city":"Thiruvananthapuram","state":"Kerala","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Dr. Vishwanath Karad MIT World Peace University","city":"Pune","state":"Maharashtra","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Easwari Engineering College","city":"Chennai","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Galgotias University","city":"Gautam Budh Nagar","state":"Uttar Pradesh","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Gandhi Institute of Technology And Management (GITAM)","city":"Visakhapatnam","state":"Andhra Pradesh","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Guru Gobind Singh Indraprastha University","city":"New Delhi","state":"Delhi","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Hindustan Institute of Technology and Science (HITS)","city":"Chennai","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Indian Institute of Information Technology Allahabad","city":"Prayagraj","state":"Uttar Pradesh","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"IIIT"},{"id":"","name":"Indian Institute of Technology Goa","city":"Ponda","state":"Goa","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"IIT"},{"id":"","name":"Jawaharlal Nehru Technological University","city":"Kakinada","state":"Andhra Pradesh","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Jaypee Institute of Information Technology","city":"Noida","state":"Uttar Pradesh","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Karunya Institute of Technology and Sciences","city":"Coimbatore","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Kongu Engineering College","city":"Perundurai","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"KPR Institute of Engineering and Technology","city":"Coimbatore","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Maharishi Markandeshwar","city":"Ambala","state":"Haryana","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Mahindra University","city":"Hyderabad","state":"Telangana","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Manav Rachna International Institute of Research & Studies","city":"Faridabad","state":"Haryana","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Maulana Azad National Urdu University","city":"Hyderabad","state":"Telangana","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"National Institute of Food Technology, Enterprenurship & Management","city":"Sonipat","state":"Haryana","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"National Institute of Food Technology, Entrepreneurship and Management - Thanjavur (NIFTEM - Thanjavur)","city":"Thanjavur","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"National Institute of Technology Agartala","city":"Agratala","state":"Tripura","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"NIT"},{"id":"","name":"National Institute of Technology Arunachal Pradesh","city":"Itanagar","state":"Arunachal Pradesh","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"NIT"},{"id":"","name":"National Institute of Technology Goa","city":"Cuncolim","state":"Goa","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"NIT"},{"id":"","name":"National Institute of Technology Mizoram","city":"Aizawl","state":"Mizoram","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"NIT"},{"id":"","name":"National Institute of Technology Nagaland","city":"Dimapur","state":"Nagaland","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"NIT"},{"id":"","name":"Nirma University","city":"Ahmedabad","state":"Gujarat","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Nitte Meenakshi Institute of Technology","city":"Bengaluru","state":"Karnataka","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"NIT"},{"id":"","name":"Noida Institute of Engineering & Technology","city":"Greater Noida","state":"Uttar Pradesh","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Pandit Dwarka Prasad Mishra Indian Institute of Information Technology, Design and Manufacturing (IIITDM) Jabalpur","city":"Jabalpur","state":"Madhya Pradesh","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"IIT"},{"id":"","name":"PES University","city":"Bengaluru","state":"Karnataka","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"PSG Institute of Technology and Applied Research","city":"Coimbatore","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"University"},{"id":"","name":"Punjab Engineering College (Deemed to be University), Chandigarh","city":"Chandigarh","state":"Chandigarh","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"R.V. College of Engineering","city":"Bengaluru","state":"Karnataka","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Rajalakshmi Engineering College","city":"Chennai","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Sharda University","city":"Greater Noida","state":"Uttar Pradesh","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Shoolini University of Biotechnology and Management Sciences","city":"Solan","state":"Himachal Pradesh","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Siddaganga Institute of Technology","city":"Tumkur","state":"Karnataka","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"SVKM`s Narsee Monjee Institute of Management Studies","city":"Mumbai","state":"Maharashtra","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"The Northcap University","city":"Gurugram","state":"Haryana","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Thiagarajar College of Engineering","city":"Madurai","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"University College of Engineering","city":"Hyderabad","state":"Telangana","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"University of Allahabad","city":"Prayagraj","state":"Uttar Pradesh","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Veermata Jijabai Technological Institute, (VJTI, Mumbai)","city":"Mumbai","state":"Maharashtra","score":null,"rank":null,"band":"Rank 101-150","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Amity University Rajasthan,Jaipur","city":"Jaipur","state":"Rajasthan","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"B. S. Abdur Rahman Crescent Institute of Science and Technology","city":"Chennai","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"B.M.S. College of Engineering","city":"Bengaluru","state":"Karnataka","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Bharati Vidyapeeth Deemed University College of Engineering","city":"Pune","state":"Maharashtra","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"C M R Institute of Technology","city":"Bengaluru","state":"Karnataka","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"CGC College of Engineering, Landran","city":"Sahibzada Ajit Singh Nagar","state":"Punjab","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Chaitanya Bharathi Institute of Technology","city":"Hyderabad","state":"Telangana","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"CVR College of Engineering","city":"Ibrahimpatan","state":"Telangana","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Dayalbagh Educational Institute","city":"Agra","state":"Uttar Pradesh","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Dr. D. Y. Patil Institute of Technology","city":"Pune","state":"Maharashtra","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Dr. M. G. R. Educational and Research Institute","city":"Chennai","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"G. L. A. University","city":"Mathura","state":"Uttar Pradesh","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"G.L.Bajaj Institute of Technology and Management","city":"Greater Noida","state":"Uttar Pradesh","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Goka Raju Ranga Raju Institute of Engineering & Technology","city":"Hyderabad","state":"Telangana","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Guru Ghasidas Vishwavidyalaya","city":"Bilaspur (Chhattisgarh)","state":"Chhattisgarh","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Indian Institute of Information Technology, Design & Manufacturing, Kancheepuram","city":"Chennai","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"IIIT"},{"id":"","name":"Institute of Aeronautical Engineering","city":"Hyderabad","state":"Telangana","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Institute of Engineering & Management","city":"Kolkata","state":"West Bengal","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Integral University","city":"Lucknow","state":"Uttar Pradesh","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Islamic University of Science & Technology, Pulwama","city":"Pulwama","state":"Jammu and Kashmir","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"J. C. Bose University of Science and Technology, YMCA","city":"Faridabad","state":"Haryana","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Jawaharlal Nehru Technological University","city":"Ananthapuramu","state":"Andhra Pradesh","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"JSPM's Rajarshi Shahu College of Engineering","city":"Pune","state":"Maharashtra","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"KIET Group of Institutions","city":"Ghaziabad","state":"Uttar Pradesh","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"KLE Technological University","city":"Dharwad","state":"Karnataka","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Kumaraguru College of Technology","city":"Coimbatore","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Maulana Abul Kalam Azad University of Technology","city":"Nadia","state":"West Bengal","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Mepco Schlenk Engineering College","city":"Sivakasi","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"National Institute of Technology Manipur","city":"Imphal","state":"Manipur","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"NIT"},{"id":"","name":"National Institute of Technology Sikkim","city":"South Sikkim","state":"Sikkim","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"NIT"},{"id":"","name":"National Institute of Technology Uttarakhand","city":"Srinagar (Garhwal)","state":"Uttarakhand","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"NIT"},{"id":"","name":"New Horizon College of Engineering","city":"Bengaluru","state":"Karnataka","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"NMAM Institute of Technology","city":"Nitte, Udupi","state":"Karnataka","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"North Eastern Regional Institute of Science & Technology","city":"Itanagar","state":"Arunachal Pradesh","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"R.M.K. Engineering College","city":"Thiruvallur","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Ramdeobaba University, Nagpur","city":"Nagpur","state":"Maharashtra","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Shri Mata Vaishno Devi University","city":"Katra","state":"Jammu and Kashmir","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Sona College of Technology","city":"Salem","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Sri Ramakrishna Engineering College","city":"Coimbatore","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Sri Sai Ram Institute of Technology","city":"Chennai","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Sri Sairam Engineering College","city":"Kancheepuram","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Tezpur University","city":"Tezpur","state":"Assam","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"The National Institute of Engineering","city":"Mysuru","state":"Karnataka","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Vallurupalli Nageswara Rao Vignana Jyothi Institute of Engineering and Technology","city":"Hyderabad","state":"Telangana","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Vardhaman College of Engineering","city":"Rangareddy","state":"Telangana","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Veer Surendra Sai University of Technology","city":"Sambalpur","state":"Odisha","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Velagapudi Ramakrishna Siddhartha Engineering College","city":"Vijayawada","state":"Andhra Pradesh","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Vels Institute of Science Technology and Advanced Studies (VISTAS)","city":"Chennai","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Vignan Institute of Technology and Science","city":"Yadadri-Bhuvangiri","state":"Telangana","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Visvesvaraya Technological University","city":"Belgaum","state":"Karnataka","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Yeshwantrao Chavan College of Engineering","city":"Nagpur","state":"Maharashtra","score":null,"rank":null,"band":"Rank 151 to 200","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Aditya Institute of Technology and Management","city":"Tekkali","state":"Andhra Pradesh","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Aditya University","city":"Surampalem","state":"Andhra Pradesh","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Ajeenkya D Y Patil University","city":"Pune","state":"Maharashtra","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Amity University Patna","city":"Patna","state":"Bihar","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Amity University, Gwalior","city":"Gwalior","state":"Madhya Pradesh","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Amity University, Jharkhand","city":"Ranchi","state":"Jharkhand","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Annamalai University","city":"Annamalainagar","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Army Institute of Technology","city":"Pune","state":"Maharashtra","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"B I T SINDRI","city":"Dhanbad","state":"Jharkhand","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"BML Munjal University","city":"Gurgaon","state":"Haryana","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"BMS Institute of Technology & Management","city":"Bengaluru","state":"Karnataka","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Centurion University of Technology and Management","city":"Paralakhemundi","state":"Odisha","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Chandigarh Engineering College Jhanjeri","city":"Sahibzada Ajit Singh Nagar","state":"Punjab","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"CMR College of Engineering & Technology","city":"Hyderabad","state":"Telangana","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"CMR Technical Campus","city":"Hyderabad","state":"Telangana","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"College of Engineering & Technology, Bhubaneswar","city":"Bhubaneswar","state":"Odisha","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"University"},{"id":"","name":"Dayananda Sagar College of Engineering","city":"Bengaluru","state":"Karnataka","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Dhirubhai Ambani Institute of Information and Communication Technology","city":"Gandhinagar","state":"Gujarat","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Dr. Shyama Prasad Mukherjee International Institute of Information Technology, Naya Raipur","city":"Raipur","state":"Chhattisgarh","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"E.G.S. Pillay Engineering College","city":"Nagapattinam","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"G. H. Raisoni College of Engineering, Nagpur","city":"Nagpur","state":"Maharashtra","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"G. Narayanamma Institute of Technology & Science for Women","city":"Hyderabad","state":"Telangana","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Galgotias College of Engineering & Technology","city":"Greater Noida","state":"Uttar Pradesh","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Gandhi Engieering College (GEC)","city":"Bhubaneswar","state":"Odisha","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Gandhi Institute for Technological Advancement (GITA), Bhubaneswar","city":"Bhubaneswar","state":"Odisha","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"University"},{"id":"","name":"GIET University, Gunupur","city":"Gunupur","state":"Odisha","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"GMR Institute of Technology","city":"Rajam","state":"Andhra Pradesh","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Godavari Institute of Engineering & Technology","city":"Rajahmundry","state":"Andhra Pradesh","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Guru Jambheshwar University of Science and Technology, Hissar","city":"Hisar","state":"Haryana","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Harcourt Butler Technical University","city":"Kanpur Nagar","state":"Uttar Pradesh","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Hindusthan College of Engineering and Technology","city":"Coimbatore","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"IES College of Technology, Bhopal","city":"Bhopal","state":"Madhya Pradesh","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Indian Institute of Information Technology Guwahati","city":"Guwahati","state":"Assam","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"IIIT"},{"id":"","name":"Indian Institute of Petroleum & Energy","city":"Visakhapatnam","state":"Andhra Pradesh","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Indira Gandhi Delhi Technical University for Women","city":"Delhi","state":"Delhi","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Jamia Hamdard","city":"New Delhi","state":"Delhi","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Jaypee University of Information Technology","city":"Solan","state":"Himachal Pradesh","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"JIS College of Engineering","city":"Kalyani","state":"West Bengal","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Jss Academy Of Technical Education, Noida","city":"Gautam Budh Nagar","state":"Uttar Pradesh","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"JSS Science and Technology University","city":"Mysuru","state":"Karnataka","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"K. Ramakrishnan College of Engineering","city":"Samayapuram","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"K. Ramakrishnan College of Technology","city":"Tiruchirappalli","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Kakatiya Institute of Technology & Science","city":"Warangal","state":"Telangana","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Kalaignar Karunanidhi Institute of Technology","city":"Coimbatore","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Karpagam College of Engineering","city":"Coimbatore","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Lakshmi Narain College of Technology","city":"Bhopal","state":"Madhya Pradesh","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"M.Kumarasamy College of Engineering","city":"Karur","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Madanapalle Institute of Technology & Science","city":"Madanapalle","state":"Andhra Pradesh","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Maharaja Sayajirao University of Baroda","city":"Vadodara","state":"Gujarat","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Maharshi Dayanand University, Rohtak","city":"Rohtak","state":"Haryana","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Maharshi Karve Stree Shikshan Samstha's Cummins College of Engineering for Women","city":"Pune","state":"Maharashtra","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Mahatama Jyotiba Phule Rohikhand University, Bareilly","city":"Bareilly","state":"Uttar Pradesh","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Malla Reddy Engineering College","city":"Hyderabad","state":"Telangana","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Malla Reddy Engineering College for Women (Autonomous)","city":"Hyderabad","state":"Telangana","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Manav Rachna University","city":"Faridabad","state":"Haryana","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Marwadi University","city":"Rajkot","state":"Gujarat","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"MIT Art, Design and Technology University, Pune","city":"Pune","state":"Maharashtra","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"MLR Institute of Technology","city":"Hyderabad","state":"Telangana","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Narula Institute of Technology","city":"Kolkata","state":"West Bengal","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"National Engineering College","city":"Kovilpatti","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"National Institute of Advanced Manufacturing Technology, Ranchi","city":"Ranchi","state":"Jharkhand","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"National Institute Of Technology, Andhra Pradesh","city":"Tadepalligudem","state":"Andhra Pradesh","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"NIT"},{"id":"","name":"P E S College of Engineering, MANDYA","city":"Mandya","state":"Karnataka","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Padmashree Dr. D. Y. Patil Vidyapeeth, Mumbai","city":"Mumbai","state":"Maharashtra","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Panimalar Engineering College","city":"Thiruvallur","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Pimpri Chinchwad College of Engineering","city":"Pune","state":"Maharashtra","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Prasad V Potluri Siddhartha Institue of Technology","city":"Vijayawada","state":"Andhra Pradesh","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Presidency University , Bengaluru","city":"Bengaluru","state":"Karnataka","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Prince Shri Venkateshwara Padmavathy Engineering College","city":"Kancheepuram","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"PSNA College of Engineering and Technology, Dindigul","city":"Dindigul","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Puducherry Technological University","city":"Puducherry","state":"Pondicherry","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"QIS College of Engineering & Technology","city":"Ongole","state":"Andhra Pradesh","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"R. M. K. College of Engineering and Technology","city":"Thiruvallur","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"R.M.D Engineering College","city":"Thiruvallur","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Rabindranath Tagore University","city":"Raisen","state":"Madhya Pradesh","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Rajalakshmi Institute of Technology","city":"Thiruvallur","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Rajeev Gandhi Memorial College of Engineering & Technology","city":"Nandyal","state":"Andhra Pradesh","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Rathinam Technical Campus","city":"Coimbatore","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Reva University","city":"Bengaluru","state":"Karnataka","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Saveetha Engineering College","city":"Sriperumbudur","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"University"},{"id":"","name":"Shri Vile Parle Kelavani Mandal`s Dwarkadas J. Sanghvi College of Engineering","city":"Mumbai Suburban","state":"Maharashtra","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Sikkim Manipal Institute of Technology (SMIT)","city":"Rangpo","state":"Sikkim","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"University"},{"id":"","name":"Silicon University,Odisha, Bhubaneswar","city":"Bhubaneswar","state":"Odisha","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"University"},{"id":"","name":"SNS College of Technology","city":"Coimbatore","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Sree Vidyanikethan Engineering College","city":"Tirupati","state":"Andhra Pradesh","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Sri Eshwar College of Engineering","city":"Coimbatore","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Sri Manakula Vinayagar Engineering College","city":"Puducherry","state":"Pondicherry","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Sri Venkateswara College of Engineering","city":"Sriperumbudur","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Sri Venkateswara College of Engineering and Technology","city":"Chittoor","state":"Andhra Pradesh","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Sri Venkateswara College of Engineering, Tirupati","city":"Tirupati","state":"Andhra Pradesh","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Sri Venkateswara University","city":"Tirupati","state":"Andhra Pradesh","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"St. Joseph`s Institute of Technology","city":"Chennai","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"St. Josephs College of Engineering","city":"Chennai","state":"Tamil Nadu","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Teerthanker Mahaveer University","city":"Moradabad","state":"Uttar Pradesh","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"The LNM Institute of Information Technology, Jaipur","city":"Jaipur","state":"Rajasthan","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Uttaranchal University","city":"Dehradun","state":"Uttarakhand","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Vidya Jyothi Institute of Technology","city":"Hyderabad","state":"Telangana","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Vignan`s Institute of Information Technology","city":"Visakhapatnam","state":"Andhra Pradesh","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"},{"id":"","name":"Walchand College of Engineering","city":"Sangli","state":"Maharashtra","score":null,"rank":null,"band":"Rank 201 to 300","url":"https://www.nirfindia.org","type":"Private"}];

// ── helpers ──
function getRankBadge(r){
  if(r===1) return '<span class="rank-badge r1">1</span>';
  if(r===2) return '<span class="rank-badge r2">2</span>';
  if(r===3) return '<span class="rank-badge r3">3</span>';
  if(r&&r<=10) return `<span class="rank-badge r-top">${r}</span>`;
  if(r) return `<span class="rank-badge r-top" style="font-size:0.8rem">${r}</span>`;
  return '<span class="rank-badge r-band">&mdash;</span>';
}
function getScore(s){
  if(!s) return '<span style="color:var(--muted);font-size:0.78rem">Band ranked</span>';
  return `<div class="score-cell"><div class="score-track"><div class="score-fill" style="width:${((s/90)*100).toFixed(0)}%"></div></div><span class="score-val">${s.toFixed(2)}</span></div>`;
}
function getType(t){return `<span class="type-tag type-${t}">${t}</span>`;}
function getSt(s){return `<span class="state-tag">${s}</span>`;}
function getBand(b){
  const m={"Rank 1 -100":"band-1","Rank 101-150":"band-2","Rank 151 to 200":"band-3","Rank 201 to 300":"band-4"};
  const l={"Rank 1 -100":"1&ndash;100","Rank 101-150":"101&ndash;150","Rank 151 to 200":"151&ndash;200","Rank 201 to 300":"201&ndash;300"};
  return `<span class="band-badge ${m[b]||'band-4'}">${l[b]||b}</span>`;
}
function getLink(url){
  const d=url.replace(/https?:\/\//,'').split('/')[0];
  return `<a class="web-link" href="${url}" target="_blank" rel="noopener">&#127760; ${d.substring(0,18)}</a>`;
}
function makeTopCard(r,i){
  const rc=i===0?'gold':i===1?'silver':i===2?'bronze':'';
  return `<div class="top-card">
    <div class="tc-rank ${rc}">#${r.rank||'&mdash;'}</div>
    <div class="tc-body">
      <div class="tc-name">${r.name}</div>
      <div class="tc-city">${r.city}, ${r.state} &middot; ${r.type}</div>
      ${r.score?`<div class="tc-score">${r.score.toFixed(2)}<span style="font-size:0.75rem;color:var(--muted)">/100</span></div>`:''}
      <a class="tc-web" href="${r.url}" target="_blank">&#127760; Visit Website</a>
    </div>
  </div>`;
}

// ── Build state data ──
function buildStateData(){
  const map={};
  DATA.forEach(r=>{
    if(!map[r.state]) map[r.state]={state:r.state,total:0,in100:0,in150:0,bestRank:null,bestScore:null,scores:[],colleges:[]};
    const s=map[r.state];
    s.total++;
    s.colleges.push(r);
    if(r.rank&&r.rank<=100) s.in100++;
    if(r.rank&&r.rank<=150) s.in150++;
    if(r.rank&&(s.bestRank===null||r.rank<s.bestRank)) s.bestRank=r.rank;
    if(r.score){s.scores.push(r.score);if(s.bestScore===null||r.score>s.bestScore)s.bestScore=r.score;}
  });
  Object.values(map).forEach(s=>{
    s.avgScore=s.scores.length?+(s.scores.reduce((a,b)=>a+b,0)/s.scores.length).toFixed(2):0;
    s.colleges.sort((a,b)=>{if(a.rank&&b.rank)return a.rank-b.rank;if(a.rank)return -1;if(b.rank)return 1;return a.name.localeCompare(b.name);});
  });
  return Object.values(map).sort((a,b)=>b.total-a.total);
}
const STATE_DATA=buildStateData();

// ── QUADRANT CHART ──
let qChart=null;

function getAxisVal(s,key){
  if(key==='in100') return s.in100;
  if(key==='in150') return s.in150;
  if(key==='bestScore') return s.bestScore||0;
  if(key==='avgScore') return s.avgScore||0;
  if(key==='total') return s.total;
  return s.total;
}
function getAxisLabel(key){
  const labels={
    in100:'Colleges in Rank 1\u201C100',in150:'Colleges in Rank 1\u2013150',
    bestScore:'Best NIRF Score',avgScore:'Avg NIRF Score (ranked)',total:'Total Colleges'
  };
  return labels[key]||key;
}

function redrawQuadrant(){
  if(!document.getElementById('quadrantChart')) return;
  const yKey=document.getElementById('yAxisSel').value;
  const xKey=document.getElementById('xAxisSel').value;
  const labelMode=document.getElementById('labelSel').value;

  const pts=STATE_DATA.map(s=>{
    const x=getAxisVal(s,xKey);
    const y=getAxisVal(s,yKey);
    const br=s.bestRank?Math.max(7,Math.min(30,32-(s.bestRank/100)*22)):5;
    return {x,y,r:br,_s:s,_st:s.state};
  });

  const allX=pts.map(p=>p.x).sort((a,b)=>a-b);
  const allY=pts.map(p=>p.y).sort((a,b)=>a-b);
  const xMed=allX[Math.floor(allX.length/2)];
  const yMed=allY[Math.floor(allY.length/2)];

  const byQ=[[],[],[],[]]; // Elite, Efficient, Developing, Emerging
  pts.forEach(p=>{
    const hi_x=p.x>=xMed, hi_y=p.y>=yMed;
    if(hi_x&&hi_y) byQ[0].push(p);
    else if(!hi_x&&hi_y) byQ[1].push(p);
    else if(hi_x&&!hi_y) byQ[2].push(p);
    else byQ[3].push(p);
  });

  const datasets=[
    {label:'Elite (High vol \xb7 High rank)',data:byQ[0],backgroundColor:'rgba(255,107,0,0.78)',borderColor:'rgba(255,107,0,1)',borderWidth:2,hoverBorderWidth:3},
    {label:'Efficient (Low vol \xb7 High rank)',data:byQ[1],backgroundColor:'rgba(34,211,160,0.78)',borderColor:'rgba(34,211,160,1)',borderWidth:2,hoverBorderWidth:3},
    {label:'Developing (High vol \xb7 Low rank)',data:byQ[2],backgroundColor:'rgba(251,191,36,0.78)',borderColor:'rgba(251,191,36,1)',borderWidth:2,hoverBorderWidth:3},
    {label:'Emerging (Low vol \xb7 Low rank)',data:byQ[3],backgroundColor:'rgba(107,120,152,0.78)',borderColor:'rgba(107,120,152,1)',borderWidth:2,hoverBorderWidth:3},
  ];

  const top10states=STATE_DATA.slice(0,10).map(s=>s.state);

  const pluginQuadLines={
    id:'quadLines',
    afterDraw(chart){
      const {ctx,scales}=chart;
      const xS=scales.x,yS=scales.y;
      const xPx=xS.getPixelForValue(xMed);
      const yPx=yS.getPixelForValue(yMed);
      ctx.save();
      ctx.setLineDash([7,5]);
      ctx.strokeStyle='rgba(255,255,255,0.14)';
      ctx.lineWidth=1.5;
      ctx.beginPath();ctx.moveTo(xPx,yS.top);ctx.lineTo(xPx,yS.bottom);ctx.stroke();
      ctx.beginPath();ctx.moveTo(xS.left,yPx);ctx.lineTo(xS.right,yPx);ctx.stroke();
      ctx.setLineDash([]);
      // Quadrant watermark labels
      const lw=(xS.right-xS.left)/2, lh=(yS.bottom-yS.top)/2;
      ctx.font='bold 13px Arial';
      ctx.fillStyle='rgba(255,255,255,0.07)';
      ctx.textAlign='center';
      ctx.fillText('ELITE'        , xPx+lw*0.55, yS.top+26);
      ctx.fillText('EFFICIENT'    , xPx-lw*0.55, yS.top+26);
      ctx.fillText('DEVELOPING'   , xPx+lw*0.55, yS.bottom-14);
      ctx.fillText('EMERGING'     , xPx-lw*0.55, yS.bottom-14);
      ctx.restore();
    }
  };

  const pluginLabels={
    id:'stateLabels',
    afterDatasetsDraw(chart){
      const {ctx}=chart;
      chart.data.datasets.forEach((ds,di)=>{
        const meta=chart.getDatasetMeta(di);
        if(!meta.visible) return;
        ds.data.forEach((pt,pi)=>{
          const el=meta.data[pi];
          if(!el) return;
          const show=labelMode==='always'||(labelMode==='top10'&&top10states.includes(pt._st));
          if(!show) return;
          const s=pt._st;
          const short=s.length>13?s.substring(0,12)+'\u2026':s;
          const rad=el.options.radius||8;
          ctx.save();
          ctx.font='bold 9.5px Arial';
          ctx.fillStyle='rgba(255,255,255,0.88)';
          ctx.textAlign='center';
          ctx.textBaseline='top';
          ctx.shadowColor='rgba(0,0,0,0.9)';
          ctx.shadowBlur=5;
          ctx.fillText(short,el.x,el.y+rad+4);
          ctx.restore();
        });
      });
    }
  };

  if(qChart){qChart.destroy();qChart=null;}

  qChart=new Chart(document.getElementById('quadrantChart'),{
    type:'bubble',
    data:{datasets},
    options:{
      responsive:true,
      maintainAspectRatio:false,
      aspectRatio:1.8,
      interaction:{mode:'nearest',intersect:true},
      plugins:{
        legend:{
          position:'bottom',
          labels:{color:'rgba(232,237,248,0.65)',font:{size:11,family:'Arial'},boxWidth:12,padding:18}
        },
        tooltip:{
          backgroundColor:'rgba(10,13,22,0.97)',
          titleColor:'#FF6B00',bodyColor:'rgba(232,237,248,0.85)',
          borderColor:'rgba(255,107,0,0.45)',borderWidth:1,padding:14,
          callbacks:{
            title:items=>items[0]?.raw?._st||'',
            label:item=>{
              const s=item.raw?._s;
              if(!s) return '';
              return [
                ` Total colleges: ${s.total}`,
                ` In Rank 1\u2013100: ${s.in100}`,
                ` Best rank: ${s.bestRank?'#'+s.bestRank:'\u2014'}`,
                ` Best score: ${s.bestScore?s.bestScore.toFixed(2):'\u2014'}`,
                ` Avg score: ${s.avgScore?s.avgScore.toFixed(2):'\u2014'}`,
              ];
            }
          }
        }
      },
      scales:{
        x:{
          title:{display:true,text:getAxisLabel(xKey),color:'rgba(255,107,0,0.75)',font:{size:12,weight:'bold',family:'Arial'},padding:{top:8}},
          ticks:{color:'rgba(232,237,248,0.5)',font:{size:10,family:'Arial'}},
          grid:{color:'rgba(255,255,255,0.04)'},
          border:{color:'rgba(255,107,0,0.2)'}
        },
        y:{
          title:{display:true,text:getAxisLabel(yKey),color:'rgba(255,107,0,0.75)',font:{size:12,weight:'bold',family:'Arial'},padding:{bottom:8}},
          ticks:{color:'rgba(232,237,248,0.5)',font:{size:10,family:'Arial'}},
          grid:{color:'rgba(255,255,255,0.04)'},
          border:{color:'rgba(255,107,0,0.2)'}
        }
      },
      onClick(e,elements){
        if(!elements.length) return;
        const el=elements[0];
        const pt=qChart.data.datasets[el.datasetIndex].data[el.index];
        if(pt?._s) showStateDetail(pt._s);
      },
      animation:{duration:400}
    },
    plugins:[pluginQuadLines,pluginLabels]
  });
}

function showStateDetail(s){
  const card=document.getElementById('stateDetail');
  card.style.display='block';
  document.getElementById('sdTitle').textContent='\ud83d\udccd '+s.state+' \u2014 State Detail';
  document.getElementById('sdTotal').textContent=s.total;
  document.getElementById('sdIn100').textContent=s.in100;
  document.getElementById('sdBestRank').textContent=s.bestRank?'#'+s.bestRank:'\u2014';
  document.getElementById('sdBestScore').textContent=s.bestScore?s.bestScore.toFixed(2):'\u2014';
  const top5=s.colleges.slice(0,5);
  document.getElementById('sdColleges').innerHTML=
    '<strong style="color:var(--orange)">Top Colleges in '+s.state+':</strong><br>'+
    top5.map(c=>
      `${c.rank?'<strong style="color:var(--orange)">#'+c.rank+'</strong> ':''}`+
      `${c.name}${c.score?' <span style="color:var(--muted);">('+c.score.toFixed(2)+')</span>':''}<br>`
    ).join('');
  card.scrollIntoView({behavior:'smooth',block:'nearest'});
}

// ── STATE TABLE ──
let stSortKey='total',stSortDir=-1;
function sortST(key){
  if(stSortKey===key) stSortDir*=-1; else{stSortKey=key;stSortDir=-1;}
  renderStateTable([...STATE_DATA].sort((a,b)=>{
    if(key==='state') return stSortDir*a.state.localeCompare(b.state);
    if(key==='idx') return stSortDir*(STATE_DATA.indexOf(a)-STATE_DATA.indexOf(b));
    const av=a[key]??-1,bv=b[key]??-1;
    if(key==='bestRank') return stSortDir>0?(av===null?1:bv===null?-1:av-bv):(av===null?1:bv===null?-1:av-bv)*-1;
    return stSortDir*(bv-av);
  }));
}
function renderStateTable(data){
  let i=1;
  document.getElementById('stateCompBody').innerHTML=data.map(s=>{
    const best=s.colleges.find(c=>c.rank===s.bestRank);
    return `<tr>
      <td><strong style="color:var(--muted)">${i++}</strong></td>
      <td>${getSt(s.state)}</td>
      <td><strong style="color:var(--orange)">${s.total}</strong></td>
      <td><strong style="color:var(--green)">${s.in100}</strong></td>
      <td>${s.in150}</td>
      <td>${s.bestRank?`<strong>#${s.bestRank}</strong>`:'&mdash;'}</td>
      <td>${s.bestScore?`<span style="color:var(--orange);font-weight:700">${s.bestScore.toFixed(2)}</span>`:'&mdash;'}</td>
      <td>${s.avgScore?s.avgScore.toFixed(2):'&mdash;'}</td>
      <td style="font-size:0.82rem">${best?`<a href="${best.url}" target="_blank" style="color:var(--blue2);text-decoration:none">${best.name.substring(0,34)}${best.name.length>34?'&hellip;':''}</a>`:'&mdash;'}</td>
    </tr>`;
  }).join('');
}

// ── TABLE ──
let filt=[...DATA],pg=1,ps=25;
function applyF(){
  const s=document.getElementById('mainSearch').value.toLowerCase();
  const st=document.getElementById('stateFilter').value;
  const ty=document.getElementById('typeFilter').value;
  const bd=document.getElementById('bandFilter').value;
  const so=document.getElementById('sortFilter').value;
  filt=DATA.filter(r=>{
    if(s&&!r.name.toLowerCase().includes(s)&&!r.city.toLowerCase().includes(s)&&!r.state.toLowerCase().includes(s)) return false;
    if(st&&r.state!==st) return false;
    if(ty&&r.type!==ty) return false;
    if(bd&&r.band!==bd) return false;
    return true;
  });
  if(so==='rank') filt.sort((a,b)=>(a.rank||9999)-(b.rank||9999));
  else if(so==='score') filt.sort((a,b)=>(b.score||0)-(a.score||0));
  else if(so==='name') filt.sort((a,b)=>a.name.localeCompare(b.name));
  else if(so==='state') filt.sort((a,b)=>a.state.localeCompare(b.state));
  pg=1;renderTbl();renderPag();
  document.getElementById('tblCount').textContent=filt.length+' institutions';
}
function renderTbl(){
  const sl=filt.slice((pg-1)*ps,pg*ps);
  document.getElementById('mainBody').innerHTML=sl.map(r=>`<tr>
    <td>${getRankBadge(r.rank)}</td>
    <td><span style="font-weight:700">${r.name}</span></td>
    <td>${getScore(r.score)}</td>
    <td>${getBand(r.band)}</td>
    <td style="font-size:0.82rem">${r.city}</td>
    <td>${getSt(r.state)}</td>
    <td>${getType(r.type)}</td>
    <td>${getLink(r.url)}</td>
  </tr>`).join('');
}
function renderPag(){
  const tot=Math.ceil(filt.length/ps);
  const pages=[1,pg-1,pg,pg+1,tot].filter(p=>p>=1&&p<=tot);
  const uniq=[...new Set(pages)].sort((a,b)=>a-b);
  let html='',prev=-1;
  uniq.forEach(p=>{
    if(prev!==-1&&p-prev>1) html+='<span style="color:var(--muted);padding:0 4px">&hellip;</span>';
    html+=`<button class="pg-btn ${p===pg?'active':''}" data-pg="${p}">${p}</button>`;
    prev=p;
  });
  html+=`<span class="pg-info">Page ${pg}/${tot} &middot; ${filt.length} results</span>`;
  document.getElementById('pagination').innerHTML=html;
  document.querySelectorAll('.pg-btn[data-pg]').forEach(b=>
    b.addEventListener('click',()=>{pg=+b.dataset.pg;renderTbl();renderPag();}));
}

// ── COMPARE ──
function buildCompareDrops(){
  const ranked=DATA.filter(r=>r.rank).sort((a,b)=>a.rank-b.rank);
  const opts=ranked.map(r=>`<option value="${r.rank}">#${r.rank} ${r.name.substring(0,40)}</option>`).join('');
  ['cmpA','cmpB','cmpC'].forEach(id=>{
    document.getElementById(id).innerHTML='<option value="">Select&hellip;</option>'+opts;
    document.getElementById(id).onchange=runCompare;
  });
}
function runCompare(){
  const ids=['cmpA','cmpB','cmpC'].map(id=>document.getElementById(id).value).filter(Boolean);
  if(ids.length<2){document.getElementById('cmpResult').innerHTML='<p style="color:var(--muted);text-align:center;padding:24px">Select at least 2 colleges</p>';return;}
  const cols=ids.map(id=>DATA.find(r=>r.rank==id)).filter(Boolean);
  const rows=[
    ['Rank',r=>r.rank?`<strong style="color:var(--orange)">#${r.rank}</strong>`:'Band'],
    ['Score',r=>r.score?`<span style="color:var(--orange);font-weight:700">${r.score.toFixed(2)}</span>`:'Not scored'],
    ['Band',r=>getBand(r.band)],['Type',r=>getType(r.type)],['State',r=>getSt(r.state)],
    ['City',r=>r.city],['Website',r=>`<a href="${r.url}" target="_blank" style="color:var(--blue2)">Visit &rarr;</a>`],
  ];
  document.getElementById('cmpResult').innerHTML=`<div style="overflow-x:auto">
    <table style="width:100%;border-collapse:collapse">
      <thead><tr>
        <th style="padding:10px 14px;background:rgba(255,107,0,0.08);color:var(--orange);font-size:0.78rem;text-transform:uppercase;text-align:left">Parameter</th>
        ${cols.map(c=>`<th style="padding:10px 14px;background:rgba(255,107,0,0.08);color:#fff;font-size:0.82rem;text-align:center">${c.name.substring(0,35)}${c.name.length>35?'&hellip;':''}</th>`).join('')}
      </tr></thead>
      <tbody>${rows.map(([lbl,fn])=>`<tr>
        <td style="padding:9px 14px;color:var(--muted);font-size:0.82rem;border-bottom:1px solid rgba(255,255,255,0.04)">${lbl}</td>
        ${cols.map(c=>`<td style="padding:9px 14px;text-align:center;border-bottom:1px solid rgba(255,255,255,0.04)">${fn(c)}</td>`).join('')}
      </tr>`).join('')}</tbody>
    </table></div>`;
}

// ── STATE DRILLDOWN ──
let selState='';
function buildStatePills(){
  const cnt={};DATA.forEach(r=>cnt[r.state]=(cnt[r.state]||0)+1);
  const sorted=Object.entries(cnt).sort((a,b)=>b[1]-a[1]);
  document.getElementById('statePills').innerHTML=
    [['','All States',DATA.length],...sorted.map(([s,c])=>[s,s,c])].map(([s,lbl,c])=>
    `<div class="sp${s===selState?' sel':''}" data-st="${s}">
      <div class="sp-num">${c}</div>
      <div class="sp-name">${lbl.length>13?lbl.substring(0,12)+'\u2026':lbl}</div>
    </div>`).join('');
  document.querySelectorAll('.sp').forEach(el=>el.addEventListener('click',()=>{
    selState=el.dataset.st;buildStatePills();updateSV();
  }));
}
function updateSV(){
  const band=document.getElementById('svBand').value;
  let items=selState?DATA.filter(r=>r.state===selState):DATA;
  if(band) items=items.filter(r=>r.band===band);
  items=[...items].sort((a,b)=>{
    if(a.rank&&b.rank) return a.rank-b.rank;
    if(a.rank) return -1;if(b.rank) return 1;
    return a.name.localeCompare(b.name);
  });
  document.getElementById('svCount').textContent=
    `${items.length} institution${items.length!==1?'s':''}${selState?' \u00b7 '+selState:''}${band?' \u00b7 '+band:''}`;
  document.getElementById('svCards').innerHTML=items.map(r=>`
    <div class="top-card" style="padding:14px;gap:10px">
      <div style="font-size:1.4rem;font-weight:700;color:var(--orange);min-width:36px;line-height:1">${r.rank?'#'+r.rank:'\u2014'}</div>
      <div style="flex:1">
        <div style="font-weight:700;font-size:0.87rem;margin-bottom:3px">${r.name}</div>
        <div style="font-size:0.72rem;color:var(--muted);margin-bottom:5px">${r.city} &middot; ${getType(r.type)} ${getBand(r.band)}</div>
        ${r.score?`<div style="font-weight:700;color:var(--orange);font-size:1rem">${r.score.toFixed(2)}</div>`:''}
        <a class="tc-web" href="${r.url}" target="_blank">&#127760; Website</a>
      </div>
    </div>`).join('');
}

// ── CHARTS ──
const CI={};
function dc(id){if(CI[id]){CI[id].destroy();delete CI[id];}}
const COLS=['#FF6B00','#FF8C38','#FBBF24','#22D3A0','#2563EB','#A78BFA','#F43F5E','#06B6D4','#10B981','#EC4899','#1A4FAA','#F59E0B'];
const CD={
  plugins:{
    legend:{labels:{color:'rgba(232,237,248,0.55)',font:{size:11,family:'Arial'},boxWidth:12}},
    tooltip:{backgroundColor:'rgba(10,13,22,0.97)',titleColor:'#FF6B00',bodyColor:'rgba(232,237,248,0.8)',borderColor:'rgba(255,107,0,0.35)',borderWidth:1,padding:10}
  },
  scales:{
    x:{ticks:{color:'rgba(232,237,248,0.5)',font:{size:10,family:'Arial'}},grid:{color:'rgba(255,255,255,0.04)'},border:{color:'rgba(255,107,0,0.15)'}},
    y:{ticks:{color:'rgba(232,237,248,0.5)',font:{size:10,family:'Arial'}},grid:{color:'rgba(255,255,255,0.04)'},border:{color:'rgba(255,107,0,0.15)'}},
  },
  animation:{duration:400}
};

function drawAnalytics(){
  if(typeof Chart==='undefined') return;
  Chart.defaults.font.family='Arial';

  dc('top20Bar');
  const t20=DATA.filter(r=>r.rank&&r.rank<=20).sort((a,b)=>a.rank-b.rank);
  CI['top20Bar']=new Chart(document.getElementById('top20Bar'),{
    type:'bar',
    data:{
      labels:t20.map(r=>'#'+r.rank+' '+r.name.replace('Indian Institute of Technology','IIT').replace('National Institute of Technology','NIT').substring(0,22)),
      datasets:[{label:'NIRF Score',data:t20.map(r=>r.score||0),
        backgroundColor:t20.map((_,i)=>i===0?'#FFD700':i===1?'#C0C0C0':i===2?'#CD7F32':i<10?'#FF6B00':'rgba(255,107,0,0.6)'),
        borderColor:'rgba(255,255,255,0.1)',borderWidth:1,borderRadius:4}]
    },
    options:{...CD,indexAxis:'y',responsive:true,maintainAspectRatio:false,
      plugins:{...CD.plugins,legend:{display:false},tooltip:{...CD.plugins.tooltip,callbacks:{label:ctx=>' Score: '+ctx.parsed.x.toFixed(2)}}},
      scales:{x:{...CD.scales.x,min:40,max:92},y:{...CD.scales.y,ticks:{...CD.scales.y.ticks,font:{size:9,family:'Arial'}}}}
    }
  });

  dc('typeAvgBar');
  const am={};
  DATA.filter(r=>r.score).forEach(r=>{if(!am[r.type])am[r.type]=[];am[r.type].push(r.score);});
  const tps=['IIT','IISc','BITS','NIT','IIIT','University','Private','Govt'].filter(t=>am[t]);
  CI['typeAvgBar']=new Chart(document.getElementById('typeAvgBar'),{
    type:'bar',
    data:{labels:tps,datasets:[{label:'Avg Score',data:tps.map(t=>+(am[t].reduce((a,b)=>a+b,0)/am[t].length).toFixed(2)),backgroundColor:COLS,borderColor:'rgba(255,255,255,0.1)',borderWidth:1,borderRadius:4}]},
    options:{...CD,responsive:true,maintainAspectRatio:false,
      plugins:{...CD.plugins,legend:{display:false},tooltip:{...CD.plugins.tooltip,callbacks:{label:ctx=>' Avg: '+ctx.parsed.y.toFixed(2)}}},
      scales:{x:{...CD.scales.x},y:{...CD.scales.y,min:30,max:90}}
    }
  });

  dc('histBar');
  const scores=DATA.filter(r=>r.score).map(r=>r.score);
  const bins=[[40,50],[50,55],[55,60],[60,65],[65,70],[70,75],[75,80],[80,92]];
  CI['histBar']=new Chart(document.getElementById('histBar'),{
    type:'bar',
    data:{labels:bins.map(([lo,hi])=>lo+'\u2013'+hi),
      datasets:[{label:'Colleges',data:bins.map(([lo,hi])=>scores.filter(s=>s>=lo&&s<hi).length),
        backgroundColor:['#1A4FAA','#2563EB','#22D3A0','#FBBF24','#FF8C38','#FF6B00','#F59E0B','#FFD700'],
        borderColor:'rgba(255,255,255,0.1)',borderWidth:1,borderRadius:4}]
    },
    options:{...CD,responsive:true,maintainAspectRatio:false,
      plugins:{...CD.plugins,legend:{display:false}},
      scales:{
        x:{...CD.scales.x,title:{display:true,text:'Score Range',color:'rgba(255,255,255,0.4)',font:{size:10}}},
        y:{...CD.scales.y,title:{display:true,text:'Colleges',color:'rgba(255,255,255,0.4)',font:{size:10}}}
      }
    }
  });

  dc('state100Bar');
  const s100={};
  DATA.filter(r=>r.rank&&r.rank<=100).forEach(r=>s100[r.state]=(s100[r.state]||0)+1);
  const top12=Object.entries(s100).sort((a,b)=>b[1]-a[1]).slice(0,12);
  CI['state100Bar']=new Chart(document.getElementById('state100Bar'),{
    type:'bar',
    data:{labels:top12.map(s=>s[0]),datasets:[{label:'In Rank 1\u2013100',data:top12.map(s=>s[1]),backgroundColor:COLS,borderColor:'rgba(255,255,255,0.1)',borderWidth:1,borderRadius:4}]},
    options:{...CD,indexAxis:'y',responsive:true,maintainAspectRatio:false,
      plugins:{...CD.plugins,legend:{display:false}},
      scales:{x:{...CD.scales.x},y:{...CD.scales.y,ticks:{...CD.scales.y.ticks,font:{size:10,family:'Arial'}}}}
    }
  });

  dc('typeRangeBar');
  const scT=['IIT','NIT','BITS','IIIT','University','Private'];
  const scD=scT.map(t=>DATA.filter(r=>r.score&&r.type===t).map(r=>r.score));
  CI['typeRangeBar']=new Chart(document.getElementById('typeRangeBar'),{
    type:'bar',
    data:{labels:scT,datasets:[
      {label:'Min',data:scT.map((_,i)=>scD[i].length?Math.min(...scD[i]):0),backgroundColor:'rgba(37,99,235,0.55)',borderRadius:4,borderWidth:1},
      {label:'Avg',data:scT.map((_,i)=>{const v=scD[i];return v.length?+(v.reduce((a,b)=>a+b,0)/v.length).toFixed(1):0;}),backgroundColor:'rgba(255,107,0,0.8)',borderRadius:4,borderWidth:1},
      {label:'Max',data:scT.map((_,i)=>scD[i].length?Math.max(...scD[i]):0),backgroundColor:'rgba(251,191,36,0.7)',borderRadius:4,borderWidth:1},
    ]},
    options:{...CD,responsive:true,maintainAspectRatio:false,
      plugins:{...CD.plugins,legend:{...CD.plugins.legend,display:true,position:'top'}},
      scales:{x:{...CD.scales.x},y:{...CD.scales.y,min:30,max:92}}
    }
  });

  dc('typeDoughnut');
  const tc={};DATA.forEach(r=>tc[r.type]=(tc[r.type]||0)+1);
  const tkeys=Object.keys(tc).sort((a,b)=>tc[b]-tc[a]);
  CI['typeDoughnut']=new Chart(document.getElementById('typeDoughnut'),{
    type:'doughnut',
    data:{labels:tkeys,datasets:[{data:tkeys.map(k=>tc[k]),backgroundColor:COLS,borderColor:'#131825',borderWidth:2}]},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{labels:{color:'rgba(232,237,248,0.6)',font:{size:11,family:'Arial'},boxWidth:12}},
        tooltip:{backgroundColor:'rgba(10,13,22,0.97)',titleColor:'#FF6B00',bodyColor:'rgba(232,237,248,0.8)',borderColor:'rgba(255,107,0,0.35)',borderWidth:1,padding:10,
          callbacks:{label:ctx=>` ${ctx.label}: ${ctx.parsed} colleges`}}
      },animation:{duration:400}
    }
  });
}

function drawOverview(){
  if(typeof Chart==='undefined') return;
  Chart.defaults.font.family='Arial';
  const sc={};DATA.forEach(r=>sc[r.state]=(sc[r.state]||0)+1);
  const top12=Object.entries(sc).sort((a,b)=>b[1]-a[1]).slice(0,12);
  dc('stateChart');
  CI['stateChart']=new Chart(document.getElementById('stateChart'),{
    type:'bar',data:{labels:top12.map(s=>s[0]),datasets:[{label:'Colleges',data:top12.map(s=>s[1]),backgroundColor:COLS,borderRadius:4,borderWidth:1,borderColor:'rgba(255,255,255,0.1)'}]},
    options:{...CD,responsive:true,maintainAspectRatio:false,
      plugins:{...CD.plugins,legend:{display:false}},
      scales:{x:{...CD.scales.x,ticks:{...CD.scales.x.ticks,maxRotation:40,font:{size:9}}},y:{...CD.scales.y}}
    }
  });
  const tc={};DATA.forEach(r=>tc[r.type]=(tc[r.type]||0)+1);
  const tkeys=Object.keys(tc).sort((a,b)=>tc[b]-tc[a]);
  dc('typeChart');
  CI['typeChart']=new Chart(document.getElementById('typeChart'),{
    type:'doughnut',data:{labels:tkeys,datasets:[{data:tkeys.map(k=>tc[k]),backgroundColor:COLS,borderColor:'#131825',borderWidth:2}]},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{labels:{color:'rgba(232,237,248,0.55)',font:{size:10,family:'Arial'},boxWidth:10}},
        tooltip:{backgroundColor:'rgba(10,13,22,0.97)',titleColor:'#FF6B00',bodyColor:'rgba(232,237,248,0.8)',borderColor:'rgba(255,107,0,0.35)',borderWidth:1}
      },animation:{duration:400}
    }
  });
  const scores=DATA.filter(r=>r.score).map(r=>r.score);
  const bins=[[40,50],[50,55],[55,60],[60,65],[65,70],[70,75],[75,80],[80,92]];
  dc('scoreChart');
  CI['scoreChart']=new Chart(document.getElementById('scoreChart'),{
    type:'bar',data:{labels:bins.map(([lo,hi])=>lo+'\u2013'+hi),
      datasets:[{label:'Colleges',data:bins.map(([lo,hi])=>scores.filter(s=>s>=lo&&s<hi).length),
        backgroundColor:['#1A4FAA','#2563EB','#22D3A0','#FBBF24','#FF8C38','#FF6B00','#F59E0B','#FFD700'],
        borderRadius:4,borderWidth:1,borderColor:'rgba(255,255,255,0.1)'}]
    },
    options:{...CD,responsive:true,maintainAspectRatio:false,
      plugins:{...CD.plugins,legend:{display:false}},
      scales:{x:{...CD.scales.x,ticks:{...CD.scales.x.ticks,font:{size:9}}},y:{...CD.scales.y}}
    }
  });
  dc('top10Chart');
  const t10=DATA.filter(r=>r.rank&&r.rank<=10).sort((a,b)=>a.rank-b.rank);
  CI['top10Chart']=new Chart(document.getElementById('top10Chart'),{
    type:'bar',data:{
      labels:t10.map(r=>r.name.replace('Indian Institute of Technology','IIT').replace('National Institute of Technology','NIT').substring(0,22)),
      datasets:[{label:'NIRF Score',data:t10.map(r=>r.score||0),
        backgroundColor:t10.map((_,i)=>i===0?'#FFD700':i===1?'#C0C0C0':i===2?'#CD7F32':'#FF6B00'),
        borderRadius:4,borderWidth:1,borderColor:'rgba(255,255,255,0.1)'}]
    },
    options:{...CD,responsive:true,maintainAspectRatio:false,
      plugins:{...CD.plugins,legend:{display:false},tooltip:{...CD.plugins.tooltip,callbacks:{label:ctx=>' Score: '+ctx.parsed.y.toFixed(2)}}},
      scales:{x:{...CD.scales.x,ticks:{...CD.scales.x.ticks,maxRotation:35,font:{size:9}}},y:{...CD.scales.y,min:60,max:92}}
    }
  });
}

// ── NAV ──
function showSection(id){
  document.querySelectorAll('.section').forEach(s=>s.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b=>b.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  document.getElementById('nb-'+id).classList.add('active');
  const raf2=fn=>requestAnimationFrame(()=>requestAnimationFrame(fn));
  if(id==='analytics') raf2(drawAnalytics);
  if(id==='overview'||id==='top10') raf2(drawOverview);
  if(id==='statechart') raf2(()=>{redrawQuadrant();renderStateTable([...STATE_DATA]);});
  if(id==='stateview'){buildStatePills();updateSV();}
}

// ── INIT ──
window.addEventListener('DOMContentLoaded',()=>{
  const states=[...new Set(DATA.map(r=>r.state))].sort();
  document.getElementById('stateFilter').innerHTML='<option value="">All States</option>'+states.map(s=>`<option>${s}</option>`).join('');
  ['mainSearch','stateFilter','typeFilter','bandFilter','sortFilter'].forEach(id=>{
    document.getElementById(id).addEventListener(id==='mainSearch'?'input':'change',applyF);
  });
  document.getElementById('svBand').addEventListener('change',updateSV);
  applyF();
  const t5=DATA.filter(r=>r.rank&&r.rank<=5).sort((a,b)=>a.rank-b.rank);
  document.getElementById('top5Cards').innerHTML=t5.map((r,i)=>makeTopCard(r,i)).join('');
  const t10=DATA.filter(r=>r.rank&&r.rank<=10).sort((a,b)=>a.rank-b.rank);
  document.getElementById('top10Cards').innerHTML=t10.map((r,i)=>makeTopCard(r,i)).join('');
  const t11=DATA.filter(r=>r.rank&&r.rank>10&&r.rank<=20).sort((a,b)=>a.rank-b.rank);
  document.getElementById('top11Cards').innerHTML=t11.map((r,i)=>makeTopCard(r,i+10)).join('');
  buildCompareDrops();
  buildStatePills();
  requestAnimationFrame(()=>requestAnimationFrame(drawOverview));
});



// ---- next <script> block ----


	const heightObserver = new ResizeObserver(([{ contentRect }]) => {
		window.parent.postMessage({ action: 'iframeHeightUpdated', height: contentRect.height, id: 'z_WxKa' }, '*');
	});

	heightObserver.observe(document.documentElement);
