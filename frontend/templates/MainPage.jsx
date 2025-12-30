import { useState, useEffect, useCallback } from "react";
import axios from 'axios'
import "./css/style.css"
function MainPage() {
    // Состояния компонентов меняющихся
    const [search, Setsearch] = useState("");
    const [category, Setcategory] = useState("");
    const [minPrice, SetminPrice] = useState(0);
    const [maxPrice, SetmaxPrice] = useState(0);
    const [courses, Setcourses] = useState([]);
    const [sort, Setsort] = useState("");
    const [page, setPage] = useState(1)
    const [loading, setLoading] = useState(false)
    const [hasMore, sethasMore] =useState(false)

    // Главная функция которая включает в себя пагинацию, реализацию элементов фильтров
    const fetchFunction = useCallback( async (reset_courses = false, pageNumber) => {
      const params ={
        page: pageNumber,
        limit: 12
      }
      if (search) params.search = search;
      if (category) params.category = category;
      if (minPrice) params.min_price = minPrice;
      if (maxPrice) params.max_price = maxPrice;
      if (sort) params.sort = sort;

      const {data} = await axios.get("http://127.0.0.1:8000/courses", {params}); //Главный запрос

      Setcourses(prev => (reset_courses ? data : [...prev, ...data])) 
      sethasMore(data.length === 12)
    }, [search, category, minPrice, maxPrice, sort]);

    // Функция для загрузки следующей страницы
    const loadMore = () => {
      const nextPage = page + 1
      setPage(nextPage);
      fetchFunction(false, nextPage);
    }

    // Вызов функции при изменении одного из состояний
    useEffect(() => {
      setPage(1)
      sethasMore(true)
      fetchFunction(true, 1)
    }, [search, category, minPrice, maxPrice, sort])



  // Сам шаблон jsx 
  return (
    <>
      <section className="filters">
        <input type="text" id="search" placeholder="Поиск курсов..." value={search} onChange={e => {
            Setsearch(e.target.value)
        }} />

        <div className="categories">
          <label><input type="checkbox" value="Programming" checked={category === "Программирование"} onChange={e => Setcategory(e.target.checked ? "Программирование" : "")}/>Программирование</label>
          <label><input type="checkbox" value="Data" checked={category === "Дизайн"} onChange={e => Setcategory( e.target.checked ?"Дизайн" : "")}/>Дизайн</label>
          <label><input type="checkbox" value="Design" checked={category === "Дата аналитика"} onChange={e => Setcategory(e.target.checked ? "Дата аналитика" : "")}/>Дата аналитика</label>
        </div>

        <div className="sort">
          <label>Сортировка:
            <select id="sort" onChange={e => {
              Setsort(e.target.value)
            }}>
              <option value="price_asc">Цена ↑</option>
              <option value="price_desc" >Цена ↓</option>
              <option value="popularity">Популярность</option>
            </select>
          </label>
        </div>
      </section>

      <section className="courses-grid" id="courses-grid">
        {courses.map(course => {
          return (
          <div className="course-card">
          <img src={course.image} alt="Course Image" />
          <h2>{course.name}</h2>
          <p>{course.description}</p>
          <h3>{course.category}</h3>
          <p className="price">{course.price}Тг</p>
          <p>{course.customers} покупателей</p>
        </div>
        )
        })}

        {hasMore && !loading && (
          <button onClick={loadMore}>Загрузить еще</button>
        )}

        { loading && <p>Загрузка...</p>}
      </section>
    </>
  );
}

export default MainPage;
