
import React from 'react';

class Pagination extends React.Component {
  handlePageClick = (e) => {
    const { onPageChange } = this.props;
    e.preventDefault();
    onPageChange(parseInt(e.target.getAttribute('page')));
  };

  handlePreviousClick = (e) => {
    const { onPageChange, currentPage } = this.props;
    e.preventDefault();
    onPageChange(parseInt(currentPage) - 1);
  };

  handleNextClick = (e) => {
    const { onPageChange, currentPage } = this.props;
    e.preventDefault();
    onPageChange(parseInt(currentPage) + 1);
  };

  renderNextButton(nextDisabled, handleNextClick) {
    return (
      <button type="button" disabled={nextDisabled} onClick={handleNextClick}>
        Next>
      </button>
    );
  }

  renderPrevButton(previousDisabled, handlePreviousClick) {
    return (
      <button type="button" disabled={previousDisabled} onClick={handlePreviousClick}>
        {'<Prev'}
      </button>);
  }

  renderPage(page, content, handlePageClick) {
    const { currentPage } = this.props;
    if (currentPage === page) return (<button type="button" onClick={handlePageClick} page={page} key={page}><u><b>{content}</b></u></button>);
    return (<button type="button" onClick={handlePageClick} page={page} key={page}>{content}</button>);
  }

  render() {
    const props = this.props;

    const totalItems = parseInt(props.totalItems);
    const itemsPerPage = parseInt(props.itemsPerPage);
    const currentPage = parseInt(props.currentPage);
    const numberOfPage = Math.ceil(totalItems / itemsPerPage);


    const initialized = this.renderPage(currentPage, currentPage, null);
    const pages = [initialized];
    let count = 1;
    let left = currentPage;
    let right = currentPage;
    let limit = 2;
    if (3 - currentPage > 0) {
      limit += (3 - currentPage);
    } else if (currentPage + 2 - numberOfPage > 0) {
      limit += (currentPage + 2 - numberOfPage);
    }
    while (left > 1 || right < numberOfPage) {
      if (left > 1) {
        left = currentPage - count;
        if (count <= limit || currentPage - 1 <= 4) {
          pages.unshift(this.renderPage(left, left, this.handlePageClick));
        } else if (currentPage - 1 > 4) {
          if (left > 1) {
            pages.unshift(this.renderPage(left, '...', this.handlePageClick));
          }
          pages.unshift(this.renderPage(1, 1, this.handlePageClick));
          left = 0;
        }
      }
      if (right < numberOfPage) {
        right = currentPage + count;
        if (count <= limit || numberOfPage - currentPage <= 4) {
          pages.push(this.renderPage(right, right, this.handlePageClick));
        } else if (numberOfPage - currentPage > 4) {
          if (right < numberOfPage) {
            pages.push(this.renderPage(right, '...', this.handlePageClick));
          }
          pages.push(this.renderPage(numberOfPage, numberOfPage, this.handlePageClick));
          right = numberOfPage + 1;
        }
      }
      count += 1;
    }

    const previousDisabled = currentPage === 1;
    const nextDisabled = currentPage >= numberOfPage;

    return (
      <div className="gi-Pagination">
        <div className="gi-Pagination-list">
          {this.renderPrevButton(previousDisabled, this.handlePreviousClick)}
          {pages}
          {this.renderNextButton(nextDisabled, this.handleNextClick)}
        </div>
      </div>
    );
  }
}

export default Pagination;
