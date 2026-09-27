const toggle=document.querySelector(".menu-toggle"),nav=document.querySelector("#site-nav");
if(toggle&&nav){
  const toggleLabel=toggle.querySelector(".menu-toggle-label");
  const setMenuState=open=>{
    toggle.setAttribute("aria-expanded",String(open));
    toggle.setAttribute("aria-label",open?"Zavřít hlavní menu":"Otevřít hlavní menu");
    if(toggleLabel){toggleLabel.textContent=open?"Zavřít":"Menu";}
    nav.classList.toggle("open",open);
    document.body.classList.toggle("menu-open",open);
  };
  toggle.addEventListener("click",()=>{
    const open=toggle.getAttribute("aria-expanded")==="true";
    setMenuState(!open);
  });
  nav.querySelectorAll("a").forEach(a=>a.addEventListener("click",()=>{
    setMenuState(false);
  }));
  document.addEventListener("keydown",event=>{
    if(event.key==="Escape"&&toggle.getAttribute("aria-expanded")==="true"){
      setMenuState(false);
      toggle.focus();
    }
  });
  document.addEventListener("click",event=>{
    if(toggle.getAttribute("aria-expanded")==="true"&&!nav.contains(event.target)&&!toggle.contains(event.target)){
      setMenuState(false);
    }
  });
  const desktopQuery=window.matchMedia("(min-width: 1241px)");
  desktopQuery.addEventListener("change",event=>{if(event.matches){setMenuState(false);}});
}

const documentSearch=document.querySelector("#document-search");
if(documentSearch){
  const filterButtons=[...document.querySelectorAll("[data-document-filter]")];
  const sectionBlocks=[...document.querySelectorAll("[data-document-section]")];
  const moreButtons=[...document.querySelectorAll("[data-document-more]")];
  const result=document.querySelector("#document-results");
  const expanded=new Set();
  let activeFilter="all";
  const normalize=value=>value.normalize("NFD").replace(/[\u0300-\u036f]/g,"").toLowerCase();

  const renderDocuments=()=>{
    const query=normalize(documentSearch.value.trim());
    let visibleCount=0;
    sectionBlocks.forEach(block=>{
      const category=block.dataset.documentSection;
      const categoryActive=activeFilter==="all"||activeFilter===category;
      let sectionCount=0;
      block.querySelectorAll("[data-document-item]").forEach(item=>{
        const matches=!query||normalize(item.textContent).includes(query);
        const beyondPreview=item.hasAttribute("data-document-extra");
        const visible=categoryActive&&matches&&(Boolean(query)||expanded.has(category)||!beyondPreview);
        item.hidden=!visible;
        if(visible){sectionCount+=1;visibleCount+=1;}
      });
      block.hidden=!categoryActive||(Boolean(query)&&sectionCount===0);
      const more=block.querySelector("[data-document-more]");
      if(more){
        const extraCount=block.querySelectorAll("[data-document-extra]").length;
        more.hidden=Boolean(query)||!categoryActive||extraCount===0;
        more.setAttribute("aria-expanded",String(expanded.has(category)));
        more.textContent=expanded.has(category)?"Zobrazit méně":`Zobrazit dalších ${extraCount} ${category==="projects"?"projektových podkladů":"archivních záznamů"}`;
      }
    });
    result.textContent=query?`Nalezeno ${visibleCount} ${visibleCount===1?"položka":visibleCount>=2&&visibleCount<=4?"položky":"položek"}.`:"";
  };

  filterButtons.forEach(button=>button.addEventListener("click",()=>{
    activeFilter=button.dataset.documentFilter;
    filterButtons.forEach(candidate=>{
      const active=candidate===button;
      candidate.classList.toggle("is-active",active);
      candidate.setAttribute("aria-pressed",String(active));
    });
    renderDocuments();
  }));
  moreButtons.forEach(button=>button.addEventListener("click",()=>{
    const category=button.dataset.documentMore;
    if(expanded.has(category)){expanded.delete(category);}else{expanded.add(category);}
    renderDocuments();
  }));
  documentSearch.addEventListener("input",renderDocuments);
  renderDocuments();
}
