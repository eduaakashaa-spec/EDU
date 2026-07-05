document.addEventListener("DOMContentLoaded", function() {
  const N='#0E3A8A',NI='#071A44',OR='#FF6B0A',GR='#1F8B5C',AM='#E89A1C',
        TE='#1A7A6E',RE='#C23A3A',MU='#5A6278';
  Chart.defaults.font.family="'Plus Jakarta Sans',sans-serif";

  function safeChart(id,cfg){
    const el=document.getElementById(id);
    if(!el)return;
    try{new Chart(el,cfg);}catch(e){console.warn(id,e);}
  }

  // Chart 1: IT Service vs Product vs GCC salary
  safeChart("salChart",{
    type:"bar",
    data:{
      labels:["TCS/Infosys (IT Service)","Mid-tier NIT CSE avg","NITT ECE avg 2024","GCC (Goldman/JPM)","Microsoft/Adobe India","Google/Amazon India"],
      datasets:[{
        label:"Typical Fresher CTC (Rs. LPA)",
        data:[5.5,11,21.74,32,45,65],
        backgroundColor:[RE,AM,OR,N,GR,GR],
        borderRadius:5,
      }]
    },
    options:{responsive:true,maintainAspectRatio:false,indexAxis:"y",
      scales:{
        x:{grid:{color:"rgba(14,27,61,.05)"},ticks:{callback:v=>"Rs."+v+"L",color:MU,font:{size:10}}},
        y:{grid:{display:false},ticks:{color:MU,font:{size:10}}}
      },
      plugins:{legend:{display:false},tooltip:{callbacks:{label:ctx=>" Rs."+ctx.raw+" LPA"}}}
    }
  });

  // Chart 2: Institution placement avg
  safeChart("instChart",{
    type:"bar",
    data:{
      labels:["IIIT Hyd CSE","NITT CSE","IIIT Delhi CSE","IIIT Blr CSE","NIT Rourkela CSE","NIT Durgapur CSE","NIT Delhi CSE","NIT Jmshpr CSE","IIIT Nagpur CSE","VIT/SRM CSE"],
      datasets:[{
        label:"Avg Package 2024 (Rs. LPA)",
        data:[28,27.17,19.87,28,15.5,12.5,18.87,9.5,14,7.5],
        backgroundColor:[AM,N,AM,AM,GR,MU,MU,RE,MU,RE],
        borderRadius:5,
      }]
    },
    options:{responsive:true,maintainAspectRatio:false,indexAxis:"y",
      scales:{
        x:{grid:{color:"rgba(14,27,61,.05)"},ticks:{callback:v=>"Rs."+v+"L",color:MU,font:{size:9}}},
        y:{grid:{display:false},ticks:{color:MU,font:{size:9}}}
      },
      plugins:{legend:{display:false},tooltip:{callbacks:{label:ctx=>" Rs."+ctx.raw+" LPA avg"}}}
    }
  });

  // Chart 3: ECE vs CSE at NITs
  safeChart("eceVsCseChart",{
    type:"bar",
    data:{
      labels:["NITT ECE","NITT CSE","NITC ECE","NITC EEE","NIT Rkl CSE","NIT Dgp CSE","NIT Jmshpr CSE"],
      datasets:[{
        label:"Avg Package 2024 (Rs. LPA)",
        data:[21.74,27.17,21.74,14.49,15.5,12.5,9.5],
        backgroundColor:[OR,N,OR,TE,GR,MU,RE],
        borderRadius:5,
      }]
    },
    options:{responsive:true,maintainAspectRatio:false,
      scales:{
        y:{grid:{color:"rgba(14,27,61,.05)"},ticks:{callback:v=>"Rs."+v+"L",color:MU,font:{size:9}}},
        x:{grid:{display:false},ticks:{color:MU,font:{size:9}}}
      },
      plugins:{
        legend:{display:false},
        annotation:{annotations:{line1:{type:"line",yMin:15,yMax:15,borderColor:RE,borderWidth:1.5,borderDash:[4,3],label:{content:"NIT Rourkela CSE threshold",display:true,font:{size:9}}}}},
        tooltip:{callbacks:{label:ctx=>" Rs."+ctx.raw+" LPA avg 2024"}}
      }
    }
  });

  // Chart 4: Subject count
  safeChart("subjChart",{
    type:"bar",
    data:{
      labels:["CSE","ECE","EEE","Mech","Chemical"],
      datasets:[
        {label:"Shared Foundation",data:[20,20,20,20,20],backgroundColor:"rgba(31,139,92,.5)",borderRadius:3,stack:"a"},
        {label:"Branch Core",data:[38,36,34,36,32],backgroundColor:N,borderRadius:3,stack:"a"},
        {label:"Electives/Labs",data:[22,24,22,22,20],backgroundColor:OR,borderRadius:3,stack:"a"},
      ]
    },
    options:{responsive:true,maintainAspectRatio:false,
      scales:{
        y:{grid:{color:"rgba(14,27,61,.05)"},ticks:{color:MU,font:{size:10}},title:{display:true,text:"Total subjects",color:MU,font:{size:10}}},
        x:{grid:{display:false},ticks:{color:MU,font:{size:10}}}
      },
      plugins:{legend:{labels:{font:{size:10},color:NI}},tooltip:{callbacks:{label:ctx=>" "+ctx.dataset.label+": "+ctx.raw+" subjects"}}}
    }
  });

  // Scroll reveal
  const obs=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting)e.target.classList.add("visible")}),{threshold:.08});
  document.querySelectorAll(".reveal").forEach(el=>obs.observe(el));

  // WA fab
  setTimeout(()=>document.getElementById("waFab").style.display="flex",3000);
});
