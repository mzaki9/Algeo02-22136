import React, { useEffect, useState } from 'react';
import ReactPaginate from 'react-paginate';

function Items({ currentItems}) {
    return (
      <>
        {currentItems &&
           currentItems.map((url, index) => (
            <img
            key={index}
            src={url}
            style={{
                position: 'relative',
                bottom: '10vh',
                minHeight: '100px',
                minWidth: '100px',
                maxHeight: '200px',
                maxWidth: '200px',
                marginRight: '30px', // Add some space between images
            }}
            />
        ))}
      </>
    );
  }

function PaginatedItems({ itemsPerPage, items}) {
    // Here we use item offsets; we could also use page offsets
    // following the API or data you're working with.
    const [itemOffset, setItemOffset] = useState(0);
  
    // Simulate fetching items from another resources.
    // (This could be items from props; or items loaded in a local state
    // from an API endpoint with useEffect and useState)
    const endOffset = itemOffset + itemsPerPage;
    console.log(`Loading items from ${itemOffset} to ${endOffset}`);
    const currentItems = items.slice(itemOffset, endOffset);
    const pageCount = Math.ceil(items.length / itemsPerPage);
  
    // Invoke when user click to request another page.
    const handlePageClick = (event) => {
      const newOffset = (event.selected * itemsPerPage) % items.length;
      console.log(
        `User requested page number ${event.selected}, which is offset ${newOffset}`
      );
      setItemOffset(newOffset);
    };
  
    return (
      <>
        <Items currentItems={currentItems} />
        <ReactPaginate
          breakLabel="..."
          nextLabel="next >"
          onPageChange={handlePageClick}
          pageRangeDisplayed={5}
          pageCount={pageCount}
          previousLabel="< previous"
          renderOnZeroPageCount={null}
        />
      </>
    );
  }
export default PaginatedItems;