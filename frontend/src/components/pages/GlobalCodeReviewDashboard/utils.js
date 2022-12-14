export function removeNameFromArray({ array, name }) {
  const index = array.indexOf(name);
  if (index !== -1) {
    array.splice(index, 1);
  }
  return array;
}

export function filterList({ list, listItemProperty, filter }) {
  if (filter) {
    if (listItemProperty) {
      return list.filter((listItem) =>
        listItem[listItemProperty].toLowerCase().includes(filter.toLowerCase())
      );
    }
    return list.filter((listItem) =>
      listItem.toLowerCase().includes(filter.toLowerCase())
    );
  }
  return list;
}
