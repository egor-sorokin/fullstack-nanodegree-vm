from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, engine


app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurant_menu_JSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItem=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/JSON')
def menu_item_JSON(restaurant_id, item_id):
    menuItem = session.query(MenuItem).filter_by(id=item_id).one()
    return jsonify(MenuItem=menuItem.serialize)


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurant_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)

    return render_template('restaurant/menu.html', restaurant=restaurant, items=items)


@app.route('/restaurants/<int:restaurant_id>/new-menu-item/', methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()

        flash("New menu item has been created!")

        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('items/new.html', restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/<int:item_id>/edit/', methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, item_id):
    editedItem = session.query(MenuItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']

        session.add(editedItem)
        session.commit()

        flash("Menu item has been edited!")

        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('items/edit.html', restaurant_id=restaurant_id, item_id=item_id, i=editedItem)


@app.route('/restaurants/<int:restaurant_id>/<int:item_id>/delete/', methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, item_id):
    deletedItem = session.query(MenuItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        print 'yes'
        session.delete(deletedItem)
        session.commit()

        flash("Menu item has been deleted!")

        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('items/delete.html', restaurant_id=restaurant_id, item_id=item_id, i=deletedItem)


if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
